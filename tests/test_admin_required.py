import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from users.models import User


@pytest.mark.django_db
def test_admin_can_access_dashboard(client):
    """
    Checks that an admin user can access the dashboard.
    """
    # --- 1. Setup: create an admin user ---
    User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )

    # --- 2. Action: log in and visit the dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Verification ---
    assert response.status_code == 200
    assert "Dashboard" in response.content.decode()


@pytest.mark.django_db
def test_non_admin_is_forbidden_from_dashboard(client):
    """
    Checks that a non-admin user is forbidden from accessing the dashboard.
    """
    # --- 1. Setup: create a non-admin user ---
    User.objects.create(
        username="normal_user",
        password=make_password("password123"),
        is_admin=False
    )

    # --- 2. Action: log in and visit the dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "normal_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Verification ---
    # The @admin_required decorator should return a 403 (Forbidden) status code
    assert response.status_code == 403