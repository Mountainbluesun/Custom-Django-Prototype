import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User


@pytest.fixture
def admin_user(db):
    """Creates an admin user for the tests and returns it."""
    user = User.objects.create(
        username="admin_user",
        is_admin=True
    )
    user.set_password("password123")
    user.save()
    return user


@pytest.mark.django_db
def test_company_list_view(client, admin_user):
    """Checks that the company list page displays correctly."""
    # Log in the admin
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})

    # Create a company so it shows up in the list
    Company.objects.create(name="ACME Corp")

    # Visit the page
    url = reverse('companies:list')
    response = client.get(url)

    assert response.status_code == 200
    assert "ACME Corp" in response.content.decode()


@pytest.mark.django_db
def test_company_create_view(client, admin_user):
    """Checks that the creation form correctly adds a company."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})

    url = reverse('companies:create')
    # Submit the creation form
    client.post(url, {"name": "New Company", "owner": "alice"})

    # Check that the company was created in the database
    assert Company.objects.count() == 1
    assert Company.objects.first().name == "New Company"


@pytest.mark.django_db
def test_company_edit_view(client, admin_user):
    """Checks that the edit form correctly updates a company."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    company = Company.objects.create(name="Old Name")

    url = reverse('companies:edit', kwargs={'company_id': company.id})
    # Submit the edit form
    client.post(url, {"name": "New Name", "owner": "bob"})

    # Reload the object from the database to check the change
    company.refresh_from_db()
    assert company.name == "New Name"


@pytest.mark.django_db
def test_company_delete_view(client, admin_user):
    """Checks that deletion works."""
    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    company = Company.objects.create(name="To Delete")

    assert Company.objects.count() == 1

    url = reverse('companies:delete', kwargs={'company_id': company.id})
    # Submit the deletion
    client.post(url)

    # Check that the company was correctly deleted
    assert Company.objects.count() == 0