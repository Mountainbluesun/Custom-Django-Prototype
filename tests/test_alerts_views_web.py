import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
def test_alerts_are_filtered_by_user_scope(client):
    """
    Vérifie qu'un utilisateur non-admin ne voit que les alertes
    des entreprises auxquelles il a accès.
    """
    # --- 1. On crée les données dans la base de données de test ---

    # On crée deux entreprises
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")

    # On crée un utilisateur non-admin qui n'a accès qu'à la première entreprise
    user = User.objects.create(
        username="user_scoped",
        password_hash=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company1)

    # On crée deux produits, un dans chaque entreprise
    product1 = Product.objects.create(name="Produit ACME", sku="P1", company=company1, threshold=5)
    product2 = Product.objects.create(name="Produit Globex", sku="P2", company=company2, threshold=5)

    # On met les deux produits en alerte (stock < seuil)
    Movement.objects.create(product=product1, company=company1, quantity=1, kind='IN')
    Movement.objects.create(product=product2, company=company2, quantity=2, kind='IN')

    # --- 2. On se connecte en tant qu'utilisateur restreint ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 3. On visite la page des alertes ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)

    # --- 4. On vérifie les résultats ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # L'utilisateur doit voir l'alerte pour le produit de son entreprise (ACME)
    assert "Produit ACME" in html_content
    # L'utilisateur ne doit PAS voir l'alerte pour le produit de l'autre entreprise (Globex)
    assert "Produit Globex" not in html_content