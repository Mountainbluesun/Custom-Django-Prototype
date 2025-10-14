import pytest
from users.models import User
from companies.models import Company
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_user_crud_database():
    """
    Teste le cycle complet (CRUD) pour le modèle User avec la base de données.
    """
    # --- Préparation : On a besoin d'entreprises pour lier les utilisateurs ---
    company1 = Company.objects.create(name="Entreprise 1")
    company2 = Company.objects.create(name="Entreprise 2")

    # 1. READ (initial) - La table des utilisateurs doit être vide
    assert User.objects.count() == 0

    # 2. CREATE - On crée deux utilisateurs
    u1 = User.objects.create(
        username="alice",
        email="alice@mail.com",
        password=make_password("pass1")
    )
    u1.companies.add(company1)  # On lie alice à l'entreprise 1

    u2 = User.objects.create(
        username="bob",
        email="bob@mail.com",
        password=make_password("pass2")
    )
    u2.companies.add(company2)  # On lie bob à l'entreprise 2

    assert User.objects.count() == 2

    # 3. READ - On récupère un utilisateur et on vérifie ses données
    loaded_user = User.objects.get(username="alice")
    assert loaded_user is not None
    assert loaded_user.email == "alice@mail.com"
    assert loaded_user.companies.first().name == "Entreprise 1"

    # 4. UPDATE - On modifie un utilisateur
    loaded_user.username = "alice_updated"
    loaded_user.save()

    # On recharge depuis la base de données pour être sûr
    reloaded_user = User.objects.get(id=loaded_user.id)
    assert reloaded_user.username == "alice_updated"

    # 5. DELETE - On supprime un utilisateur
    reloaded_user.delete()
    assert User.objects.count() == 1

    # On vérifie que le bon utilisateur a été supprimé
    remaining_user = User.objects.first()
    assert remaining_user.username == "bob"