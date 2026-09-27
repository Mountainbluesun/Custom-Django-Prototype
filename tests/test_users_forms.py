# File: tests/test_users_forms.py
import pytest
from src.users.forms import (
    UserCreationForm,
    UserEditForm,
    PasswordResetRequestForm,
    PasswordResetConfirmForm
)

# -------------------------------
# Tests for UserCreationForm
# -------------------------------
@pytest.mark.django_db
def test_user_creation_form_valid():
    """Form is valid when both passwords match."""
    form = UserCreationForm(data={
        "username": "alice",
        "email": "alice@example.com",
        "password": "abc123",
        "password_confirm": "abc123"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_user_creation_form_invalid_password_mismatch():
    """Form is invalid when the passwords don't match."""
    form = UserCreationForm(data={
        "username": "bob",
        "email": "bob@example.com",
        "password": "abc123",
        "password_confirm": "xyz999"
    })
    assert not form.is_valid()
    assert "Passwords do not match." in str(form.errors)

# -------------------------------
# Tests for UserEditForm
# -------------------------------

@pytest.mark.django_db
def test_user_edit_form_valid():
    """UserEditForm is valid with a username and an email."""
    form = UserEditForm(data={
        "username": "carol",
        "email": "carol@example.com"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_user_edit_form_email_optional():
    """UserEditForm stays valid even without an email."""
    form = UserEditForm(data={"username": "carol"})
    assert form.is_valid()

# -------------------------------
# Tests for PasswordResetRequestForm
# -------------------------------

@pytest.mark.django_db
def test_password_reset_request_form_valid():
    """Form is valid with a correct email address."""
    form = PasswordResetRequestForm(data={"email": "test@example.com"})
    assert form.is_valid()

@pytest.mark.django_db
def test_password_reset_request_form_invalid():
    """Form is invalid with an incorrect email."""
    form = PasswordResetRequestForm(data={"email": "not-an-email"})
    assert not form.is_valid()

# -------------------------------
# Tests for PasswordResetConfirmForm
# -------------------------------
@pytest.mark.django_db
def test_password_reset_confirm_form_valid():
    """Form is valid when both passwords match."""
    form = PasswordResetConfirmForm(data={
        "new_password": "secure123",
        "confirm_password": "secure123"
    })
    assert form.is_valid()

@pytest.mark.django_db
def test_password_reset_confirm_form_invalid():
    """Form is invalid when the passwords don't match."""
    form = PasswordResetConfirmForm(data={
        "new_password": "abc",
        "confirm_password": "xyz"
    })
    assert not form.is_valid()
    assert "Passwords do not match." in str(form.errors)