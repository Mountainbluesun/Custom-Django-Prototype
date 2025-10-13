# Fichier : src/tests/test_management_commands.py (ou un nom similaire)
import pytest
from io import StringIO
from django.core.management import call_command
from users.models import User

@pytest.mark.django_db
def test_list_users_command():
    """
    Teste la nouvelle commande list_users qui lit depuis la base de données.
    """
    # --- 1. Préparation : On crée des utilisateurs dans la base de données de test ---
    User.objects.create(username="alice", is_admin=False, is_active=True)
    User.objects.create(username="bob", is_admin=True, is_active=True)
    User.objects.create(username="eve", is_admin=False, is_active=False)

    # --- 2. Action et Vérification ---

    # Test sans filtre (doit retourner 3 utilisateurs)
    out = StringIO()
    call_command('list_users', stdout=out)
    output = out.getvalue()
    assert "alice" in output
    assert "bob" in output
    assert "eve" in output

    # Test avec le filtre --admins (doit retourner "bob")
    out = StringIO()
    call_command('list_users', '--admins', stdout=out)
    output = out.getvalue()
    assert "bob" in output
    assert "alice" not in output

    # Test avec le filtre --active (doit retourner "alice" et "bob")
    out = StringIO()
    call_command('list_users', '--active', stdout=out)
    output = out.getvalue()
    assert "alice" in output
    assert "bob" in output
    assert "eve" not in output