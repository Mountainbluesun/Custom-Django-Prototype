import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User

@pytest.mark.django_db
def test_company_list_is_filtered_by_user_scope(client):
    """
    Vérifie qu'un utilisateur non-admin ne voit que les entreprises
    auxquelles il est assigné.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---

    # On crée deux entreprises
    company_acme = Company.objects.create(name="ACME")
    company_globex = Company.objects.create(name="Globex")

    # On crée un utilisateur non-admin et on l'associe uniquement à Globex
    user = User.objects.create(
        username="user_scoped",
        password_hash=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company_globex)

    # --- 2. Action : On se connecte en tant qu'utilisateur restreint ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 3. Action : On visite la page de la liste des entreprises ---
    companies_url = reverse('companies:list')
    response = client.get(companies_url)

    # --- 4. Vérification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # L'utilisateur doit voir l'entreprise qui lui est assignée (Globex)
    assert "Globex" in html_content
    # L'utilisateur ne doit PAS voir l'autre entreprise (ACME)
    assert "ACME" not in html_content