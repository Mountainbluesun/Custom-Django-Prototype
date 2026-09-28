# File: src/inventory/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from core.auth_decorators import login_required
from core.scope import scope_for
from .forms import StockInForm, StockOutForm, StockTransferForm  # We'll use dedicated forms
from . import service as inventory_service
from companies import service as company_service
from catalog import service as catalog_service
from users import service as user_service


@login_required
def stock_list(request):
    """Displays the stock movement history."""
    user = scope_for(request)

    # Admins are not filtered (None); other users only see their own companies
    # (an empty list means "no company allowed", so no movements at all).
    company_ids = None if user.get("is_admin") else user.get("companies", [])
    movements = inventory_service.list_movements(company_ids=company_ids)

    # --- Enrich the data here ---

    # 1. Build dictionaries to look up names easily
    products = {p.id: p.name for p in catalog_service.list_products()}
    companies = {c.id: c.name for c in company_service.list_companies()}
    users = {u.id: u.username for u in user_service.list_users()}

    # 2. Attach the names to each movement
    for movement in movements:
        movement.product_name = products.get(movement.product_id, "Unknown Product")
        movement.company_name = companies.get(movement.company_id, "N/A")
        movement.user_name = users.get(movement.user_id, "System")  # <-- The line that was missing

    context = {
        "movements": movements
    }
    return render(request, "inventory/list.html", context)


@login_required
def stock_in(request):
    """Handles the stock-in form."""
    user = scope_for(request)
    if request.method == "POST":
        form = StockInForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            inventory_service.add_in(
                product_id=data['product_id'],
                quantity=data['quantity'],
                company_id=data['company_id'],
                user_id=data.get('user_id') or user.get('id'),  # Use the form's user or the logged-in one
                note=data.get('note')
            )
            messages.success(request, "Stock in recorded.")
            return redirect("inventory:list")
    else:
        form = StockInForm(user=user)

    return render(request, "inventory/form_in.html", {"form": form})


@login_required
def stock_out(request):
    """Handles the stock-out form."""
    user = scope_for(request)
    if request.method == "POST":
        form = StockOutForm(request.POST, user=user)
        if form.is_valid():
            try:
                data = form.cleaned_data
                inventory_service.add_out(
                    product_id=data['product_id'],
                    quantity=data['quantity'],
                    company_id=data['company_id'],
                    user_id=user.get('id'),
                    note=data.get('note')
                )
                messages.success(request, "Stock out recorded.")
            except ValueError as e:
                messages.error(request, str(e))  # Shows the "Insufficient stock" error
            return redirect("inventory:list")
    else:
        form = StockOutForm(user=user)

    return render(request, "inventory/form_out.html", {"form": form})


@login_required
def stock_transfer(request):
    """Handles the stock transfer form."""
    user = scope_for(request)
    if request.method == "POST":
        form = StockTransferForm(request.POST, user=user)
        if form.is_valid():
            try:
                data = form.cleaned_data
                inventory_service.add_transfer(
                    product_id=data['product_id'],
                    quantity=data['quantity'],
                    company_from_id=data['company_from_id'],
                    company_to_id=data['company_to_id'],
                    user_id=user.get('id'),
                    note=data.get('note')
                )
                messages.success(request, "Transfer recorded.")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect("inventory:list")
    else:
        form = StockTransferForm(user=user)

    return render(request, "inventory/form_transfer.html", {"form": form,})