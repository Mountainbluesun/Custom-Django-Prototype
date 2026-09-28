import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
def test_alerts_user_scoped(client):
    """
    Checks that a non-admin user only sees alerts for the
    companies they have access to.
    """
    # --- 1. Create the companies ---
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")

    # --- 2. Create a non-admin user ---
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company1)

    # --- 3. Create the products ---
    product1 = Product.objects.create(name="ACME Product", sku="P1", company=company1, threshold=5)
    product2 = Product.objects.create(name="Globex Product", sku="P2", company=company2, threshold=5)

    # --- 4. Create the movements (alert) ---
    Movement.objects.create(product=product1, company=company1, quantity=1, kind='IN')
    Movement.objects.create(product=product2, company=company2, quantity=2, kind='IN')

    # --- 5. Log the user in ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 6. Access the alerts page ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)
    assert response.status_code == 200
    html_content = response.content.decode()

    # --- 7. Content verification ---
    assert "ACME Product" in html_content
    assert "Globex Product" not in html_content


@pytest.mark.django_db
def test_alerts_admin_sees_all(client):
    """
    Checks that an admin user sees all alerts,
    regardless of company.
    """
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")
    admin = User.objects.create(username="admin", password=make_password("admin123"), is_admin=True)

    product1 = Product.objects.create(name="ACME Product", sku="P1", company=company1, threshold=5)
    product2 = Product.objects.create(name="Globex Product", sku="P2", company=company2, threshold=5)

    Movement.objects.create(product=product1, company=company1, quantity=1, kind='IN')
    Movement.objects.create(product=product2, company=company2, quantity=1, kind='IN')

    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin", "password": "admin123"})

    response = client.get(reverse('alerts:list'))
    assert response.status_code == 200
    html_content = response.content.decode()
    assert "ACME Product" in html_content
    assert "Globex Product" in html_content


@pytest.mark.django_db
def test_alerts_no_products(client):
    """
    Checks the behavior when there are no alerts.
    """
    user = User.objects.create(username="user_empty", password=make_password("password123"), is_admin=False)
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_empty", "password": "password123"})

    response = client.get(reverse('alerts:list'))
    assert response.status_code == 200
    html_content = response.content.decode()
    # No alerts displayed
    assert "No alerts." in html_content