# Fichier : src/inventory/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from core.auth_decorators import login_required
from .forms import StockInForm, StockOutForm, StockTransferForm  # On utilisera des formulaires dédiés
from . import service as inventory_service
from companies import service as company_service
from catalog import service as catalog_service
from users import service as user_service

# Fichier : src/inventory/views.py
from django.shortcuts import render
from core.auth_decorators import login_required
from . import service as inventory_service
from companies import service as company_service
from catalog import service as catalog_service
from users import service as user_service


@login_required
def stock_list(request):
    """Affiche l'historique des mouvements de stock."""
    user = request.session.get("user") or {}
    allowed_company_ids = user.get("companies", [])

    if user.get("is_admin"):
        movements = inventory_service.list_movements()
    else:
        movements = inventory_service.list_movements(company_ids=allowed_company_ids)

    # --- On enrichit les données ici ---

    # 1. On crée des dictionnaires pour trouver les noms facilement
    products = {p.id: p.name for p in catalog_service.list_products()}
    companies = {c.id: c.name for c in company_service.list_companies()}
    users = {u.id: u.username for u in user_service.list_users()}

    # 2. On ajoute les noms à chaque mouvement
    for movement in movements:
        movement.product_name = products.get(movement.product_id, "Produit Inconnu")
        movement.company_name = companies.get(movement.company_id, "N/A")
        movement.user_name = users.get(movement.user_id, "Système")  # <-- La ligne qui manquait

    context = {
        "movements": movements
    }
    return render(request, "inventory/list.html", context)


@login_required
def stock_in(request):
    """Gère le formulaire d'entrée de stock."""
    user = request.session.get("user") or {}
    if request.method == "POST":
        form = StockInForm(request.POST, user=user)
        if form.is_valid():
            data = form.cleaned_data
            inventory_service.add_in(
                product_id=data['product_id'],
                quantity=data['quantity'],
                company_id=data['company_id'],
                user_id=data.get('user_id') or user.get('id'),  # Prend l'utilisateur du formulaire ou le connecté
                note=data.get('note')
            )
            messages.success(request, "Entrée de stock enregistrée.")
            return redirect("inventory:list")
    else:
        form = StockInForm(user=user)

    return render(request, "inventory/form_in.html", {"form": form})


@login_required
def stock_out(request):
    """Gère le formulaire de sortie de stock."""
    user = request.session.get("user") or {}
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
                messages.success(request, "Sortie de stock enregistrée.")
            except ValueError as e:
                messages.error(request, str(e))  # Affiche l'erreur "Stock insuffisant"
            return redirect("inventory:list")
    else:
        form = StockOutForm(user=user)

    return render(request, "inventory/form_out.html", {"form": form})


@login_required
def stock_transfer(request):
    """Gère le formulaire de transfert de stock."""
    user = request.session.get("user") or {}
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
                messages.success(request, "Transfert enregistré.")
            except ValueError as e:
                messages.error(request, str(e))
            return redirect("inventory:list")
    else:
        form = StockTransferForm(user=user)

    return render(request, "inventory/form_transfer.html", {"form": form,})