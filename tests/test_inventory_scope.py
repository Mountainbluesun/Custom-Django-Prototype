import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
def test_stock_list_is_scoped_to_user_companies(client):
    """
    Checks that a non-admin user only sees the stock movements
    of the companies they are assigned to.
    """
    acme = Company.objects.create(name="ACME")
    globex = Company.objects.create(name="Globex")
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(globex)

    acme_product = Product.objects.create(name="ACME Product", sku="P1", company=acme)
    globex_product = Product.objects.create(name="Globex Product", sku="P2", company=globex)
    Movement.objects.create(product=acme_product, company=acme, quantity=1, kind='IN')
    Movement.objects.create(product=globex_product, company=globex, quantity=1, kind='IN')

    client.post(reverse('users:login'), {"username": "user_scoped", "password": "password123"})
    response = client.get(reverse('inventory:list'))

    assert response.status_code == 200
    html_content = response.content.decode()
    assert "Globex Product" in html_content
    assert "ACME Product" not in html_content


@pytest.mark.django_db
def test_stock_list_is_empty_for_user_without_companies(client):
    """
    Checks that a non-admin user with no company sees no movement at all.
    """
    company = Company.objects.create(name="ACME")
    product = Product.objects.create(name="ACME Product", sku="P1", company=company)
    Movement.objects.create(product=product, company=company, quantity=1, kind='IN')
    User.objects.create(
        username="user_empty",
        password=make_password("password123"),
        is_admin=False
    )

    client.post(reverse('users:login'), {"username": "user_empty", "password": "password123"})
    response = client.get(reverse('inventory:list'))

    assert response.status_code == 200
    assert "ACME Product" not in response.content.decode()


@pytest.mark.django_db
def test_stock_out_records_the_logged_in_user(client):
    """
    Checks that a stock movement is attributed to the logged-in user
    (not to "System").
    """
    company = Company.objects.create(name="ACME")
    product = Product.objects.create(name="ACME Product", sku="P1", company=company)
    admin = User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )
    Movement.objects.create(product=product, company=company, quantity=10, kind='IN')

    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    client.post(reverse('inventory:stock_out'), {
        "product_id": product.id,
        "company_id": company.id,
        "quantity": 3,
        "note": "test"
    })

    movement = Movement.objects.get(kind='OUT')
    assert movement.user_id == admin.id


def _stock_in_setup():
    company = Company.objects.create(name="ACME")
    product = Product.objects.create(name="ACME Product", sku="P1", company=company)
    other = User.objects.create(username="other_user", password=make_password("x"), is_admin=False)
    return company, product, other


@pytest.mark.django_db
def test_non_admin_cannot_record_stock_in_as_another_user(client):
    """
    Checks that a non-admin user cannot attribute a stock-in to someone else.
    """
    company, product, other = _stock_in_setup()
    user = User.objects.create(username="user_scoped", password=make_password("password123"), is_admin=False)
    user.companies.add(company)

    client.post(reverse('users:login'), {"username": "user_scoped", "password": "password123"})
    client.post(reverse('inventory:stock_in'), {
        "product_id": product.id, "company_id": company.id,
        "quantity": 1, "user_id": other.id
    })
    assert Movement.objects.count() == 0

    # Without choosing a user, the movement is recorded as the logged-in user
    client.post(reverse('inventory:stock_in'), {
        "product_id": product.id, "company_id": company.id, "quantity": 1
    })
    assert Movement.objects.get().user_id == user.id


@pytest.mark.django_db
def test_admin_can_record_stock_in_as_another_user(client):
    """
    Checks that an admin can still record a stock-in on behalf of another user.
    """
    company, product, other = _stock_in_setup()
    User.objects.create(username="admin_user", password=make_password("password123"), is_admin=True)

    client.post(reverse('users:login'), {"username": "admin_user", "password": "password123"})
    client.post(reverse('inventory:stock_in'), {
        "product_id": product.id, "company_id": company.id,
        "quantity": 1, "user_id": other.id
    })
    assert Movement.objects.get().user_id == other.id