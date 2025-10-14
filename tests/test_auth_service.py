import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from users.models import User

@pytest.mark.django_db
def test_authenticate_success():
    """Vérifie qu'un utilisateur avec un mot de passe correct est authentifié."""
    User.objects.create(
        username="alice",
        password=make_password("secret123"),
    )
    user = authenticate(username="alice", password="secret123")
    assert user is not None
    assert user.username == "alice"

@pytest.mark.django_db
def test_authenticate_wrong_password():
    """Vérifie qu'un mot de passe incorrect échoue."""
    User.objects.create(
        username="alice",
        password=make_password("secret123"),
    )
    user = authenticate(username="alice", password="badpass")
    assert user is None

@pytest.mark.django_db
def test_authenticate_unknown_user():
    """Vérifie qu'un utilisateur inconnu échoue."""
    user = authenticate(username="charlie", password="whatever")
    assert user is None
