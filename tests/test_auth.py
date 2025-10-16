import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password
from bs4 import BeautifulSoup

@pytest.mark.django_db
def test_successful_login(client):
    """Vérifie qu'un utilisateur avec de bons identifiants peut se connecter."""
    # 1. Création de l'utilisateur
    user = User.objects.create(
        username="testuser",
        is_active=True
    )
    user.set_password("password123")
    user.save()

    # 2. Soumission du formulaire de connexion
    url = reverse("users:login")
    response = client.post(url, {
        "username": "testuser",
        "password": "password123"
    }, follow=True)  # follow=True pour suivre la redirection

    # 3. Vérification du succès de la connexion
    assert response.status_code == 200

    # 4. Vérifie que l'utilisateur est bien connecté (présence du nom dans la navbar)
    html_content = response.content.decode()
    assert "testuser" in html_content  # Le nom d'utilisateur devrait apparaître dans la nav



@pytest.mark.django_db
def test_failed_login_with_wrong_password(client):
    """Vérifie qu'un utilisateur avec un mauvais mot de passe ne peut pas se connecter."""
    # Création de l'utilisateur
    user = User.objects.create(
        username="testuser",
        is_active=True
    )
    user.set_password("password123")
    user.save()

    url = reverse("users:login")
    # On envoie un mauvais mot de passe
    response = client.post(url, {
        "username": "testuser",
        "password": "wrongpassword"
    })

    # La page doit se recharger (code 200)
    assert response.status_code == 200

    # On vérifie qu'un message d'erreur est présent
    html_content = response.content.decode()
    # Le message peut être "Identifiants invalides" ou dans une alerte CSS
    assert "Identifiants invalides" in html_content or "alert-error" in html_content

