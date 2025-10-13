import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User


@pytest.fixture
def admin_user(db):
    """Crée un utilisateur admin pour les tests et le retourne."""
    return User.objects.create(
        username="admin_user",
        password_hash=make_password("password123"),
        is_admin=True
    )


@pytest.mark.django_db
def test_company_list_view(client, admin_user):
    """Vérifie que la page de liste des entreprises s'affiche."""
    # On connecte l'admin
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})

    # On crée une entreprise pour qu'elle apparaisse dans la liste
    Company.objects.create(name="ACME Corp")

    # On visite la page
    url = reverse('companies:list')
    response = client.get(url)

    assert response.status_code == 200
    assert "ACME Corp" in response.content.decode()


@pytest.mark.django_db
def test_company_create_view(client, admin_user):
    """Vérifie que le formulaire de création ajoute bien une entreprise."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})

    url = reverse('companies:create')
    # On soumet le formulaire de création
    client.post(url, {"name": "Nouvelle Entreprise", "owner": "alice"})

    # On vérifie que l'entreprise a bien été créée dans la base de données
    assert Company.objects.count() == 1
    assert Company.objects.first().name == "Nouvelle Entreprise"


@pytest.mark.django_db
def test_company_edit_view(client, admin_user):
    """Vérifie que le formulaire d'édition modifie bien une entreprise."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    company = Company.objects.create(name="Ancien Nom")

    url = reverse('companies:edit', kwargs={'company_id': company.id})
    # On soumet le formulaire d'édition
    client.post(url, {"name": "Nouveau Nom", "owner": "bob"})

    # On recharge l'objet depuis la base de données pour vérifier la modification
    company.refresh_from_db()
    assert company.name == "Nouveau Nom"


@pytest.mark.django_db
def test_company_delete_view(client, admin_user):
    """Vérifie que la suppression fonctionne."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    company = Company.objects.create(name="À Supprimer")

    assert Company.objects.count() == 1

    url = reverse('companies:delete', kwargs={'company_id': company.id})
    # On soumet la suppression
    client.post(url)

    # On vérifie que l'entreprise a bien été supprimée
    assert Company.objects.count() == 0
