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
    # --- 1. On crée les données directement dans la base de données de test ---

    # On crée une entreprise et un utilisateur admin
    company = Company.objects.create(name="Test Co")
    user = User.objects.create(
        username="testuser",
        password_hash=make_password("password123"),
        is_admin=True
    )
    user.companies.add(company)

    # On crée un produit avec un seuil d'alerte de 10
    product = Product.objects.create(
        name="Produit en Alerte",
        sku="SKU-ALERT",
        company=company,
        threshold=10
    )
    # On fait une entrée de 5, ce qui est inférieur au seuil de 10
    Movement.objects.create(product=product, company=company, quantity=5, kind='IN')

    # --- 2. On se connecte en utilisant le formulaire de connexion ---
    login_url = reverse('users:login')
    client.post(login_url, {'username': 'testuser', 'password': 'password123'})

    # --- 3. On visite la page des alertes ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)

    # --- 4. On vérifie les résultats ---
    assert response.status_code == 200
    # On vérifie que le nom du produit est bien sur la page
    assert "Produit en Alerte" in response.content.decode()
    # On vérifie que le stock (5) et le seuil (10) sont bien affichés dans le tableau
    # Note: la recherche "<td>5</td>" est simple mais peut être fragile. C'est suffisant pour commencer.
    assert "<td>5</td>" in response.content.decode()
    assert "<td>10</td>" in response.content.decode()