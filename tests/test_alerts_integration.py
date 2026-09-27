import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_alerts_view_shows_product_under_threshold(client):
    """
    Checks that the alerts page displays a product whose stock is below threshold.
    """
    # --- 1. Create the data directly in the test database ---

    # Create a company and an admin user
    company = Company.objects.create(name="Test Co")
    user = User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_admin=True
    )
    user.companies.add(company)

    # Create a product with an alert threshold of 10
    product = Product.objects.create(
        name="Product on Alert",
        sku="SKU-ALERT",
        company=company,
        threshold=10
    )
    # Add a stock-in of 5, which is below the threshold of 10
    Movement.objects.create(product=product, company=company, quantity=5, kind='IN')

    # --- 2. Log in using the login form ---
    login_url = reverse('users:login')
    client.post(login_url, {'username': 'testuser', 'password': 'password123'})

    # --- 3. Visit the alerts page ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)

    # --- 4. Check the results ---
    assert response.status_code == 200
    html_content = response.content.decode()
    # Check that the product name is indeed on the page
    assert "Product on Alert" in html_content
    # Check that the stock (5) and the threshold (10) are correctly displayed in the table
    # Note: the "<td>5</td>" search is simple but can be fragile. Good enough to start with.
    assert "<td>5</td>" in html_content
    assert "<td>10</td>" in html_content