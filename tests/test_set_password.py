import pytest
from django.core.management import call_command
from django.contrib.auth.hashers import make_password, check_password
from users.models import User

@pytest.mark.django_db
def test_set_password_command():
    """
    Tests the new set_password command that changes the password in the database.
    """
    # --- 1. Setup: create a user with an old password ---
    user = User.objects.create(
        username="alice",
        password=make_password("old_password")
    )

    # Check that the old password works
    assert check_password("old_password", user.password) is True

    # --- 2. Action: call the command to change the password ---
    new_password = "new_password_123"
    call_command('set_password', user.username, new_password)

    # --- 3. Verification ---
    # Reload the user from the database to get the latest info
    user.refresh_from_db()

    # Check that the new password works
    assert check_password(new_password, user.password) is True
    # Check that the old password no longer works
    assert check_password("old_password", user.password) is False