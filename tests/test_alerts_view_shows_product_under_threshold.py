import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement

@pytest.mark.django_db
def test_alerts_view_shows_product_under_threshold(client):
    """
    Vérifie que la page des alertes affiche bien un produit sous le seuil d’alerte.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---

    # On crée une entreprise et un utilisateur admin
    company = Company.objects.create(name="TestCorp")
    user = User.objects.create(
        username="test_admin",
        password_hash=make_password("password123"),
        is_admin=True
    )
    user.companies.add(company)

    # On crée un produit avec un seuil de 10
    product = Product.objects.create(
        name="ProduitTest",
        sku="SKU-TEST",
        company=company,
        threshold=10
    )

    # On crée un mouvement pour que le stock soit à 5 (sous le seuil)
    Movement.objects.create(product=product, company=company, quantity=5, kind='IN')

    # --- 2. Action : On se connecte et on visite la page ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "test_admin", "password": "password123"})

    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)

    # --- 3. Vérification ---
    assert response.status_code == 200
    html = response.content.decode("utf-8")

    # On vérifie que les informations sont bien présentes dans la page
    assert "ProduitTest" in html
    assert "<td>5</td>" in html   # La quantité en stock
    assert "<td>10</td>" in html  # Le seuil