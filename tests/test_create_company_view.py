import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User
from django.contrib.auth.hashers import make_password

@pytest.mark.django_db
def test_create_company_view(client):
    """
    Vérifie que le formulaire de création ajoute bien une entreprise à la base de données.
    """
    # --- 1. Préparation : on crée un utilisateur admin ---
    User.objects.create(
        username="admin_user",
        password_hash=make_password("password123"),
        is_admin=True
    )

    # --- 2. Action : on se connecte en tant qu'admin ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    # --- 3. Action : on soumet le formulaire de création d'entreprise ---
    create_url = reverse('companies:create')
    client.post(create_url, {"name": "Nouvelle Entreprise SQL"})

    # --- 4. Vérification : on vérifie dans la base de données ---
    assert Company.objects.count() == 1
    assert Company.objects.first().name == "Nouvelle Entreprise SQL"