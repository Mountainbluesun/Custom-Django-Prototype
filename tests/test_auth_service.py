import pytest
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password
from users.models import User

@pytest.mark.django_db
def test_authenticate_success():
    """Checks that a user with the correct password is authenticated."""
    User.objects.create(
        username="alice",
        password=make_password("secret123"),
    )
    user = authenticate(username="alice", password="secret123")
    assert user is not None
    assert user.username == "alice"

@pytest.mark.django_db
def test_authenticate_wrong_password():
    """Checks that an incorrect password fails."""
    User.objects.create(
        username="alice",
        password=make_password("secret123"),
    )
    user = authenticate(username="alice", password="badpass")
    assert user is None

@pytest.mark.django_db
def test_authenticate_unknown_user():
    """Checks that an unknown user fails."""
    user = authenticate(username="charlie", password="whatever")
    assert user is None