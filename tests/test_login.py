import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from users.models import User


@pytest.mark.xfail(reason="Temporarily disabled - Django session to be revisited")
@pytest.mark.django_db
def test_login_success_redirects_and_sets_session(client):
    """
    POST /users/login/ with correct credentials:
    - redirects to 'home'
    - sets 'user' in the session
    """
    # --- 1. Setup: create the user in the test database ---
    User.objects.create(
        username="admin",
        password=make_password("base20025"),
        is_admin=True,
        is_active=True
    )

    # --- 2. Action: simulate submitting the login form ---
    login_url = reverse('users:login')
    response = client.post(
        login_url,
        {"username": "admin", "password": "base20025"},
        follow=True, # follow=True automatically follows the redirect
    )

    # --- 3. Verification ---
    # Check that we land on the home page after the redirect
    assert response.status_code == 200
    assert response.resolver_match.view_name == 'home' # Checks that we're on the 'home' view

    # Check that the session was created correctly
    session = client.session
    assert "user" in session
    assert session["user"]["username"] == "admin"
    assert session["user"]["is_admin"] is True

@pytest.mark.django_db
def test_login_fail_stays_on_login_and_no_session_user(client):
    """
    POST /users/login/ with the wrong password:
    - stays on the login page (200)
    - does not set 'user' in the session
    """
    # Setup: create the user
    User.objects.create(
        username="admin",
        password=make_password("base20025"),
    )

    # Action: try to log in with the wrong password
    login_url = reverse('users:login')
    response = client.post(
        login_url,
        {"username": "admin", "password": "WRONG_PASSWORD"},
    )

    # Verification: we should stay on the login page, with no redirect
    assert response.status_code == 200
    session = client.session
    assert "user" not in session
    # Check that the page does contain the "Login" title
    assert "Login" in response.content.decode()