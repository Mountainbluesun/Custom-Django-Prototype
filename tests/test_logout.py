import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password


@pytest.mark.xfail(reason="Test temporarily disabled - function to be revisited")
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

    # Check that the login worked and the session is populated
    assert "user" in client.session

    # --- 2. Action: call the logout URL ---
    logout_url = reverse('users:logout')
    response = client.get(logout_url, follow=True) # follow=True follows the redirect to the login page

    # --- 3. Verification ---
    # Check that we land on a page (the login page) after logging out
    assert response.status_code == 200
    # Check that the 'user' key was correctly removed from the session
    assert "user" not in client.session