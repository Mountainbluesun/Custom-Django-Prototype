import pytest
from users.models import User
from companies.models import Company
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_user_crud_database():
    """
    Tests the full CRUD cycle for the User model with the database.
    """
    # --- Setup: we need companies to link the users to ---
    company1 = Company.objects.create(name="Company 1")
    company2 = Company.objects.create(name="Company 2")

    # 1. READ (initial) - The user table should be empty
    assert User.objects.count() == 0

    # 2. CREATE - Create two users
    u1 = User.objects.create(
        username="alice",
        email="alice@mail.com",
        password=make_password("pass1")
    )
    u1.companies.add(company1)  # Link alice to company 1

    u2 = User.objects.create(
        username="bob",
        email="bob@mail.com",
        password=make_password("pass2")
    )
    u2.companies.add(company2)  # Link bob to company 2

    assert User.objects.count() == 2

    # 3. READ - Retrieve a user and check its data
    loaded_user = User.objects.get(username="alice")
    assert loaded_user is not None
    assert loaded_user.email == "alice@mail.com"
    assert loaded_user.companies.first().name == "Company 1"

    # 4. UPDATE - Modify a user
    loaded_user.username = "alice_updated"
    loaded_user.save()

    # Reload from the database to make sure
    reloaded_user = User.objects.get(id=loaded_user.id)
    assert reloaded_user.username == "alice_updated"

    # 5. DELETE - Delete a user
    reloaded_user.delete()
    assert User.objects.count() == 1

    # Check that the right user was deleted
    remaining_user = User.objects.first()
    assert remaining_user.username == "bob"