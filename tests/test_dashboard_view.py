import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
def test_dashboard_view_loads_for_admin(client):
    """
    Checks that the dashboard loads correctly for an admin user.
    """
    # --- 1. Setup: create the data in the test database ---

    # Create a company, a product, and a stock movement
    company = Company.objects.create(name="ACME")
    product = Product.objects.create(name="Test Product", sku="SKU1", company=company)
    Movement.objects.create(product=product, company=company, quantity=10, kind='IN')

    # Create an admin user
    admin_user = User.objects.create(
        username="admin_user",
        password=make_password("password123"),
        is_admin=True
    )
    admin_user.companies.add(company)

    # --- 2. Action: log in as admin and visit the dashboard ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin_user", "password": "password123"})

    dashboard_url = reverse('dashboard:home')
    response = client.get(dashboard_url)

    # --- 3. Verification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # Check that the chart titles are present
    assert "Dashboard" in html_content
    assert "Stock by Company" in html_content
    assert "Activity Over the Last 6 Months" in html_content