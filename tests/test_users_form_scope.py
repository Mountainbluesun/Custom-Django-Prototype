import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User


@pytest.mark.django_db
def test_admin_can_create_user_with_role_and_companies(client):
    """
    Checks that an admin can create a user, assign the Administrator role
    and pick their companies from the creation form.
    """
    admin = User.objects.create(username="admin_user", password=make_password("password123"), is_admin=True)
    acme = Company.objects.create(name="ACME")
    globex = Company.objects.create(name="Globex")

    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    client.post(reverse('users:create'), {
        "username": "newbie",
        "email": "newbie@example.com",
        "password": "pass1234",
        "password_confirm": "pass1234",
        "is_admin": "on",
        "companies": [acme.id, globex.id],
    })

    newbie = User.objects.get(username="newbie")
    assert newbie.is_admin is True
    assert set(newbie.companies.values_list("id", flat=True)) == {acme.id, globex.id}


@pytest.mark.django_db
def test_admin_can_edit_a_user_companies_and_role(client):
    """
    Checks that editing a user updates their Administrator role and companies.
    """
    admin = User.objects.create(username="admin_user", password=make_password("password123"), is_admin=True)
    acme = Company.objects.create(name="ACME")
    globex = Company.objects.create(name="Globex")
    target = User.objects.create(username="david", password=make_password("x"), is_admin=False)
    target.companies.add(acme)

    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    client.post(reverse('users:edit', args=[target.id]), {
        "username": "david",
        "email": "",
        "is_admin": "on",
        "companies": [globex.id],
    })

    target.refresh_from_db()
    assert target.is_admin is True
    assert list(target.companies.values_list("id", flat=True)) == [globex.id]


@pytest.mark.django_db
def test_new_user_without_companies_sees_no_data(client):
    """
    End-to-end: a user created without any company still sees empty lists
    everywhere, confirming the create-form fix and the earlier scoping fix
    work together.
    """
    admin = User.objects.create(username="admin_user", password=make_password("password123"), is_admin=True)
    Company.objects.create(name="ACME")

    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    client.post(reverse('users:create'), {
        "username": "isolated",
        "email": "",
        "password": "pass1234",
        "password_confirm": "pass1234",
    })

    client.post(reverse('users:logout'))
    client.post(reverse('users:login'), {"username": "isolated", "password": "pass1234"})
    response = client.get(reverse('catalog:list'))
    assert "ACME" not in response.content.decode()