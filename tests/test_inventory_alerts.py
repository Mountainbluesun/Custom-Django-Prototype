import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement
from django.contrib.auth.hashers import make_password

@pytest.mark.django_db
def test_alerts_view_shows_product_under_threshold(client):
    """
    Vérifie que la page des alertes affiche un produit dont le stock est sous le seuil.
    """
    # --- 1. On crée les données dans la base de données de test ---
    company = Company.objects.create(name="Test Co")
    user = User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_admin=True
    )
    user.companies.add(company)

    product = Product.objects.create(
        name="Produit en Alerte",
        sku="SKU-ALERT",
        company=company,
        threshold=10
    )
    # On fait une entrée de 5, ce qui est inférieur au seuil de 10
    Movement.objects.create(product=product, company=company, quantity=5, kind='IN')

    # --- 2. On se connecte en utilisant le formulaire ---
    login_url = reverse('users:login')
    client.post(login_url, {'username': 'testuser', 'password': 'password123'})

    # --- 3. On visite la page des alertes ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)

    # --- 4. On vérifie les résultats ---
    assert response.status_code == 200
    assert "Produit en Alerte" in response.content.decode()
