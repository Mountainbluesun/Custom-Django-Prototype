# Fichier : src/catalog/views.py
from django.shortcuts import render, redirect
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.views.decorators.http import require_http_methods

from core.auth_decorators import login_required, admin_required
from .forms import ProductForm
from . import service
from . import csv_io


def _allowed_company_ids(request):
    """
    Retourne la liste des IDs d'entreprises accessibles à l'utilisateur.
    Utilise la session si disponible, sinon fallback sur le modèle User.
    """
    session_user = request.session.get("user") or {}
    from companies.models import Company

    # 🔹 Cas 1 — session avec données
    if session_user.get("is_admin"):
        return list(Company.objects.values_list('id', flat=True))
    elif session_user.get("companies"):
        return session_user["companies"]

    # 🔹 Cas 2 — fallback : user Django connecté
    user = getattr(request, "user", None)
    if user and user.is_authenticated:
        if getattr(user, "is_admin", False) or getattr(user, "is_staff", False):
            return list(Company.objects.values_list('id', flat=True))
        # si ton modèle User a une relation M2M avec Company :
        if hasattr(user, "companies"):
            return list(user.companies.values_list("id", flat=True))

    # 🔹 Par défaut — aucune entreprise accessible
    return []



@login_required
def product_list(request):
    ids = _allowed_company_ids(request)
    prods = service.list_products_by_companies(ids)

    # Enrichir chaque produit avec son stock actuel
    from inventory.service import compute_stock
    for p in prods:
        p.current_stock = compute_stock(product_id=p.id)
    print("DEBUG allowed_company_ids:", ids)
    print("DEBUG produits trouvés:", len(prods))
    for p in prods:
        print(" -", p.name, "(Company ID:", p.company_id, ")")

    return render(request, "catalog/list.html", {"products": prods})


@admin_required
def product_create(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            service.create_product(**form.cleaned_data)
            messages.success(request, "Produit créé avec succès.")
            return redirect("catalog:list")
        session_user = request.session.get("user", {}) ## Test
        print(session_user) ## Test

    else:
        form = ProductForm()

    return render(request, "catalog/form.html", {"form": form, "mode": "create"})


@admin_required
def product_edit(request, pid: int):
    product = service.get_product(pid)
    if not product:
        raise Http404("Produit non trouvé")

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            service.update_product(pid, form.cleaned_data)
            messages.success(request, f"Le produit '{product.name}' a été mis à jour.")
            return redirect("catalog:list")
    else:
        initial_data = {
            'name': product.name,
            'sku': product.sku,
            'company_id': product.company.id,  # On utilise l'ID de la relation
            'threshold': product.threshold,
        }
        form = ProductForm(initial=initial_data)

    return render(request, "catalog/form.html", {"form": form, "mode": "edit"})


@admin_required
def product_delete(request, pid: int):
    product = service.get_product(pid)
    if not product:
        raise Http404("Produit non trouvé.")

    if request.method == "POST":
        service.delete_product(pid)
        messages.success(request, f"Le produit '{product.name}' a été supprimé.")
        return redirect("catalog:list")

    return render(request, "catalog/confirm_delete.html", {"product": product})


# Les vues pour le CSV ne changent que très peu
@admin_required
def products_export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'

    products = service.list_products()
    # On transforme les objets en dictionnaires pour le CSV
    product_dicts = [
        {"name": p.name, "sku": p.sku, "company_id": p.company_id, "threshold": p.threshold}
        for p in products
    ]
    csv_io.write_products_csv(response, product_dicts)
    return response


@admin_required
@require_http_methods(["POST"])
def products_import_csv(request):
    f = request.FILES.get("csv_file")
    if not f:
        messages.error(request, "Aucun fichier transmis.")
        return redirect("catalog:list")

    try:
        rows = csv_io.read_products_csv(f)
        created = 0
        for r in rows:
            service.create_product(**r)
            created += 1
        messages.success(request, f"Import terminé : {created} produit(s) ajoutés.")
    except Exception as e:
        messages.error(request, f"Erreur lors de la lecture du fichier CSV: {e}")

    return redirect("catalog:list")


# La vue pour la page d'import ne change pas
@admin_required
def product_import_page_view(request):
    return render(request, "catalog/import_page.html")

