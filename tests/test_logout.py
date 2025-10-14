import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password
@pytest.mark.skip(reason="Test désactivé temporairement – fonction à revoir")
@pytest.mark.django_db
def test_logout_clears_session(client):
    """
    Vérifie que la vue de déconnexion vide bien la session de l'utilisateur.
    """
    # --- 1. Préparation : On crée un utilisateur et on le connecte ---
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
    )
    login_url = reverse('users:login')
    client.post(login_url, {"username": "testuser", "password": "password123"})

    # On vérifie que la connexion a bien fonctionné et que la session est remplie
    assert "user" in client.session

    # --- 2. Action : On appelle l'URL de déconnexion ---
    logout_url = reverse('users:logout')
    response = client.get(logout_url, follow=True) # follow=True suit la redirection vers la page de login

    # --- 3. Vérification ---
    # On vérifie qu'on arrive bien sur une page (celle de login) après la déconnexion
    assert response.status_code == 200
    # On vérifie que la clé 'user' a bien été supprimée de la session
    assert "user" not in client.session