import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement
from inventory import service as inventory_service

@pytest.mark.django_db
def test_stock_in_and_out_forms(client):
    """
    Teste le flux complet de soumission des formulaires d'entrée et de sortie de stock.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company = Company.objects.create(name="Test Corp")
    product = Product.objects.create(name="Produit Test", sku="SKU-TEST", company=company)
    admin_user = User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )
    admin_user.companies.add(company)

    # --- 2. Action : On se connecte en tant qu'admin ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    # --- 3. Test du formulaire d'entrée de stock (IN) ---
    stock_in_url = reverse('inventory:stock_in')
    client.post(stock_in_url, {
        "product_id": product.id,
        "company_id": company.id,
        "quantity": 10,
        "note": "Entrée initiale"
    })

    # Vérification : le stock doit être à 10
    assert inventory_service.compute_stock(product_id=product.id) == 10
    assert Movement.objects.filter(kind='IN').count() == 1

    # --- 4. Test du formulaire de sortie de stock (OUT) ---
    stock_out_url = reverse('inventory:stock_out')
    client.post(stock_out_url, {
        "product_id": product.id,
        "company_id": company.id,
        "quantity": 3,
        "note": "Vente client"
    })

    # Vérification : le stock doit être à 7 (10 - 3)
    assert inventory_service.compute_stock(product_id=product.id) == 7
    assert Movement.objects.filter(kind='OUT').count() == 1