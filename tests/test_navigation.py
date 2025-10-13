import pytest
from django.urls import reverse
from users.models import User

@pytest.fixture
def logged_in_client(client, db):
    """
    Crée un utilisateur admin, le connecte et retourne le client.
    """
    user = User.objects.create(
        username="testuser",
        is_admin=True  # donne les permissions nécessaires
    )
    user.set_password("password123")
    user.save()

    client.post(reverse('users:login'), {"username": "testuser", "password": "password123"})
    return client


@pytest.mark.django_db
def test_home_page_loads(logged_in_client):
    """Vérifie que la page d'accueil se charge correctement."""
    url = reverse('home')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_products_page_loads(logged_in_client):
    """Vérifie que la page des produits se charge correctement."""
    url = reverse('catalog:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_companies_page_loads(logged_in_client):
    """Vérifie que la page des entreprises se charge."""
    url = reverse('companies:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_page_loads(logged_in_client):
    """Vérifie que la page des stocks se charge."""
    url = reverse('inventory:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_alerts_page_loads(logged_in_client):
    """Vérifie que la page des alertes se charge."""
    url = reverse('alerts:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200
