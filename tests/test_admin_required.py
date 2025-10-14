import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from users.models import User


@pytest.mark.django_db
def test_admin_can_access_dashboard(client):
    """
    Vérifie qu'un utilisateur administrateur peut accéder au dashboard.
    """
    # --- 1. Préparation : On crée un utilisateur admin ---
    User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )

    # --- 2. Action : On se connecte et on visite le dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Vérification ---
    assert response.status_code == 200
    assert "Dashboard" in response.content.decode()


@pytest.mark.django_db
def test_non_admin_is_forbidden_from_dashboard(client):
    """
    Vérifie qu'un utilisateur non-admin est interdit d'accès au dashboard.
    """
    # --- 1. Préparation : On crée un utilisateur non-admin ---
    User.objects.create(
        username="normal_user",
        password=make_password("password123"),
        is_admin=False
    )

    # --- 2. Action : On se connecte et on visite le dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "normal_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Vérification ---
    # Le décorateur @admin_required devrait renvoyer un code 403 (Forbidden)
    assert response.status_code == 403