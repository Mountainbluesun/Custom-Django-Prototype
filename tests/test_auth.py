import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password

@pytest.mark.django_db
def test_successful_login(client):
    """Vérifie qu'un utilisateur avec de bons identifiants peut se connecter."""
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_active=True
    )

    url = reverse("users:login")
    response = client.post(url, {
        "username": "testuser",
        "password": "password123"
    })

    assert response.status_code == 302
    assert response.url == reverse("home")


@pytest.mark.django_db
def test_failed_login_with_wrong_password(client):
    """Vérifie qu'un utilisateur avec un mauvais mot de passe ne peut pas se connecter."""
    User.objects.create(
        username="testuser",
        password=make_password("password123")
    )

    url = reverse("users:login")
    response = client.post(url, {
        "username": "testuser",
        "password": "wrongpassword"
    })

    assert response.status_code == 200
    assert "Identifiants invalides" in response.content.decode()
