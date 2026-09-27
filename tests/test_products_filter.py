import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product

@pytest.mark.django_db
def test_products_are_filtered_by_user_scope(client):
    """
    Checks that a non-admin user only sees products from the
    companies they have access to.
    """
    # --- 1. Setup: create the data in the test database ---

    # Create two companies
    company_acme = Company.objects.create(name="ACME")
    company_globex = Company.objects.create(name="Globex")

    # Create a NON-ADMIN user and assign them only to Globex
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company_globex)

    # Create two products, one in each company
    Product.objects.create(name="ACME Product", sku="P1", company=company_acme, threshold=0)
    Product.objects.create(name="Globex Product", sku="P2", company=company_globex, threshold=0)

    # --- 2. Action: log in as the restricted user ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 3. Action: visit the product list page ---
    products_url = reverse('catalog:list')
    response = client.get(products_url)

    # --- 4. Verification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # The user should see the product from their company (Globex)
    assert "Globex Product" in html_content
    # The user should NOT see the product from the other company (ACME)
    assert "ACME Product" not in html_content