import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from users.models import User

@pytest.mark.django_db
def test_login_success_redirects_and_sets_session(client):
    """
    POST /users/login/ avec de bons identifiants :
    - redirige vers 'home'
    - pose 'user' dans la session
    """
    # --- 1. Préparation : On crée l'utilisateur dans la base de données de test ---
    User.objects.create(
        username="admin",
        password=make_password("base20025"),
        is_admin=True,
        is_active=True
    )

    # --- 2. Action : On simule la soumission du formulaire de connexion ---
    login_url = reverse('users:login')
    response = client.post(
        login_url,
        {"username": "admin", "password": "base20025"},
        follow=True, # follow=True suit automatiquement la redirection
    )

    # --- 3. Vérification ---
    # On vérifie qu'on arrive bien sur la page d'accueil après la redirection
    assert response.status_code == 200
    assert response.resolver_match.view_name == 'home' # Vérifie qu'on est sur la vue 'home'

    # On vérifie que la session a bien été créée
    session = client.session
    assert "user" in session
    assert session["user"]["username"] == "admin"
    assert session["user"]["is_admin"] is True

@pytest.mark.django_db
def test_login_fail_stays_on_login_and_no_session_user(client):
    """
    POST /users/login/ avec mauvais mot de passe :
    - reste sur la page de login (200)
    - ne pose pas 'user' dans la session
    """
    # Préparation : On crée l'utilisateur
    User.objects.create(
        username="admin",
        password=make_password("base20025"),
    )

    # Action : On essaie de se connecter avec un mauvais mot de passe
    login_url = reverse('users:login')
    response = client.post(
        login_url,
        {"username": "admin", "password": "WRONG_PASSWORD"},
    )

    # Vérification : On doit rester sur la page de login, sans redirection
    assert response.status_code == 200
    session = client.session
    assert "user" not in session
    # On vérifie que la page contient bien le titre "Connexion"
    assert "Connexion" in response.content.decode()