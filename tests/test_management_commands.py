# File: src/tests/test_management_commands.py (or a similar name)
import pytest
from io import StringIO
from django.core.management import call_command
from users.models import User

@pytest.mark.django_db
def test_list_users_command():
    """
    Tests the new list_users command that reads from the database.
    """
    # --- 1. Setup: create users in the test database ---
    User.objects.create(username="alice", is_admin=False, is_active=True)
    User.objects.create(username="bob", is_admin=True, is_active=True)
    User.objects.create(username="eve", is_admin=False, is_active=False)

    # --- 2. Action and Verification ---

    # Test without a filter (should return 3 users)
    out = StringIO()
    call_command('list_users', stdout=out)
    output = out.getvalue()
    assert "alice" in output
    assert "bob" in output
    assert "eve" in output

    # Test with the --admins filter (should return "bob")
    out = StringIO()
    call_command('list_users', '--admins', stdout=out)
    output = out.getvalue()
    assert "bob" in output
    assert "alice" not in output

    # Test with the --active filter (should return "alice" and "bob")
    out = StringIO()
    call_command('list_users', '--active', stdout=out)
    output = out.getvalue()
    assert "alice" in output
    assert "bob" in output
    assert "eve" not in output