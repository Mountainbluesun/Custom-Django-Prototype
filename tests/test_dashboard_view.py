import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
def test_dashboard_view_loads_for_admin(client):
    """
    Vérifie que le dashboard se charge correctement pour un utilisateur admin.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---

    # On crée une entreprise, un produit, et un mouvement de stock
    company = Company.objects.create(name="ACME")
    product = Product.objects.create(name="Produit Test", sku="SKU1", company=company)
    Movement.objects.create(product=product, company=company, quantity=10, kind='IN')

    # On crée un utilisateur admin
    admin_user = User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )
    admin_user.companies.add(company)

    # --- 2. Action : On se connecte en tant qu'admin et on visite le dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Vérification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # On vérifie que les titres des graphiques sont bien présents
    assert "Dashboard" in html_content
    assert "Stocks par entreprise" in html_content
    assert "Activité des 6 derniers mois" in html_content