from urllib import response

import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password
from bs4 import BeautifulSoup

@pytest.mark.django_db
def test_successful_login(client):
    """Vérifie qu'un utilisateur avec de bons identifiants peut se connecter."""
    # 1. Création de l'utilisateur
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_active=True
    )

    # 2. Soumission du formulaire de connexion
    url = reverse("users:login")
    response = client.post(url, {
        "username": "testuser",
        "password": "password123"
    }, follow=True)  # follow=True pour suivre la redirection

    # 3. Vérification du succès de la connexion
    assert response.status_code == 200

    # 4. Vérifie qu'un message de succès apparaît (si tu as des messages Django)
    soup = BeautifulSoup(response.content, "html.parser")
    success_alert = soup.select_one(".alert-success")
    assert success_alert is not None or "Bienvenue" in response.content.decode()


@pytest.mark.django_db
def test_failed_login_with_wrong_password(client):
    # ... (Création de l'utilisateur et envoi du formulaire) ...

    # La page doit se recharger (code 200)
    assert response.status_code == 200

    # VÉRIFICATION DU CONTENU TEXTUEL DANS LE TEMPLATE
    # Le message d'erreur standard de Django pour une mauvaise connexion est le suivant :
    assert "Veuillez entrer des identifiants valides" in response.content.decode() or \
           "identifiants invalides" in response.content.decode()

    # OPTIONNEL: Vérifiez que la liste de messages existe
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.select_one(".messages") is not None
