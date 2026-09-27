import pytest
from django.urls import reverse
from users.models import User

@pytest.fixture
def logged_in_client(client, db):
    """
    Creates an admin user, logs them in, and returns the client.
    """
    user = User.objects.create(
        username="testuser",
        is_admin=True  # grants the necessary permissions
    )
    user.set_password("password123")
    user.save()

    client.post(reverse('users:login'), {"username": "testuser", "password": "password123"})
    return client


@pytest.mark.django_db
def test_home_page_loads(logged_in_client):
    """Checks that the home page loads correctly."""
    url = reverse('home')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_products_page_loads(logged_in_client):
    """Checks that the products page loads correctly."""
    url = reverse('catalog:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_companies_page_loads(logged_in_client):
    """Checks that the companies page loads."""
    url = reverse('companies:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_inventory_page_loads(logged_in_client):
    """Checks that the inventory page loads."""
    url = reverse('inventory:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200


@pytest.mark.django_db
def test_alerts_page_loads(logged_in_client):
    """Checks that the alerts page loads."""
    url = reverse('alerts:list')
    response = logged_in_client.get(url)
    assert response.status_code == 200