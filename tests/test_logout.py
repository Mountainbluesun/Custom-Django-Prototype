import pytest
from django.contrib.auth import SESSION_KEY
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_logout_clears_session(client):
    """
    Checks that the logout view correctly clears the user's session.
    """
    # --- 1. Setup: create a user and log them in ---
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
    )
    login_url = reverse('users:login')
    client.post(login_url, {"username": "testuser", "password": "password123"})

    # Check that the login worked (the session holds the user's id)
    assert SESSION_KEY in client.session

    # --- 2. Action: call the logout URL ---
    logout_url = reverse('users:logout')
    response = client.post(logout_url, follow=True) # Django 5 logout requires POST; follow=True follows the redirect

    # --- 3. Verification ---
    # Check that we land on a page (the login page) after logging out
    assert response.status_code == 200
    # Check that the user is no longer authenticated
    assert SESSION_KEY not in client.session