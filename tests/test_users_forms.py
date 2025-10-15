# Fichier : tests/test_users_forms.py
import pytest
from src.users.forms import (
    UserCreationForm,
    UserEditForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm
)

# -------------------------------
# Tests pour UserCreationForm
# -------------------------------
@pytest.mark.django_db
def test_user_creation_form_valid():
    """Form valide si les deux mots de passe correspondent."""
    form = UserCreationForm(data={
        "username": "alice",
        "email": "alice@example.com",
        "password": "abc123",
        "password_confirm": "abc123"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_user_creation_form_invalid_password_mismatch():
    """Form invalide si les mots de passe ne correspondent pas."""
    form = UserCreationForm(data={
        "username": "bob",
        "email": "bob@example.com",
        "password": "abc123",
        "password_confirm": "xyz999"
    })
    assert not form.is_valid()
    assert "Les mots de passe ne correspondent pas." in str(form.errors)

# -------------------------------
# Tests pour UserEditForm
# -------------------------------

@pytest.mark.django_db
def test_user_edit_form_valid():
    """UserEditForm est valide avec un username et un email."""
    form = UserEditForm(data={
        "username": "carol",
        "email": "carol@example.com"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_user_edit_form_email_optional():
    """UserEditForm reste valide même sans email."""
    form = UserEditForm(data={"username": "carol"})
    assert form.is_valid()

# -------------------------------
# Tests pour PasswordResetRequestForm
# -------------------------------

@pytest.mark.django_db
def test_password_reset_request_form_valid():
    """Form valide avec une adresse e-mail correcte."""
    form = PasswordResetRequestForm(data={"email": "test@example.com"})
    assert form.is_valid()

@pytest.mark.django_db
def test_password_reset_request_form_invalid():
    """Form invalide avec un e-mail incorrect."""
    form = PasswordResetRequestForm(data={"email": "not-an-email"})
    assert not form.is_valid()

# -------------------------------
# Tests pour PasswordResetConfirmForm
# -------------------------------
@pytest.mark.django_db
def test_password_reset_confirm_form_valid():
    """Form valide si les deux mots de passe correspondent."""
    form = PasswordResetConfirmForm(data={
        "new_password": "secure123",
        "confirm_password": "secure123"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_password_reset_confirm_form_invalid():
    """Form invalide si les mots de passe ne correspondent pas."""
    form = PasswordResetConfirmForm(data={
        "new_password": "abc",
        "confirm_password": "xyz"
    })
    assert not form.is_valid()
    assert "Les mots de passe ne correspondent pas." in str(form.errors)
