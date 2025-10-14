import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product

@pytest.mark.django_db
def test_products_are_filtered_by_user_scope(client):
    """
    Vérifie qu'un utilisateur non-admin ne voit que les produits
    des entreprises auxquelles il a accès.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---

    # On crée deux entreprises
    company_acme = Company.objects.create(name="ACME")
    company_globex = Company.objects.create(name="Globex")

    # On crée un utilisateur NON-ADMIN et on l'associe uniquement à Globex
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company_globex)

    # On crée deux produits, un dans chaque entreprise
    Product.objects.create(name="Produit ACME", sku="P1", company=company_acme, threshold=0)
    Product.objects.create(name="Produit Globex", sku="P2", company=company_globex, threshold=0)

    # --- 2. Action : On se connecte en tant qu'utilisateur restreint ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 3. Action : On visite la page de la liste des produits ---
    products_url = reverse('catalog:list')
    response = client.get(products_url)

    # --- 4. Vérification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # L'utilisateur doit voir le produit de son entreprise (Globex)
    assert "Produit Globex" in html_content
    # L'utilisateur ne doit PAS voir le produit de l'autre entreprise (ACME)
    assert "Produit ACME" not in html_content
