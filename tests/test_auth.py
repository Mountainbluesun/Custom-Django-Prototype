import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password
@pytest.mark.skip(reason="Test désactivé temporairement – fonction à revoir")

@pytest.mark.django_db
def test_successful_login(client):
    """Vérifie qu'un utilisateur avec de bons identifiants peut se connecter."""
    # 1. On crée un utilisateur dans la base de données de test
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_active=True
    )

    # 2. On simule la soumission du formulaire de connexion
    url = reverse("users:login")
    response = client.post(url, {
        "username": "testuser",
        "password": "password123"
    })

    # 3. On vérifie qu'on est bien redirigé vers la page d'accueil
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
    # On envoie un mauvais mot de passe
    response = client.post(url, {
        "username": "testuser",
        "password": "wrongpassword"
    })

    # On vérifie que la page se recharge (code 200) et qu'on n'est pas redirigé
    assert response.status_code == 200
    # On vérifie que la page contient un message d'erreur
    assert "Identifiants invalides" in response.content.decode()