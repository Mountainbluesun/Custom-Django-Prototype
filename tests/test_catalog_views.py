import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User
from catalog.models import Product
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_product_list_view_for_logged_in_user(client):
    """Checks that a logged-in user can see the correct products."""

    # 1. Prepare the data in the test database
    company1 = Company.objects.create(name="TestCorp 1")
    user = User.objects.create(
        username='testuser',
        password=make_password('password123'),  # Use a known password
        is_admin=True
    )
    user.companies.add(company1)
    Product.objects.create(name="Visible Product", sku="A1", company=company1)

    # 2. The test logs in using your login view
    login_url = reverse('users:login')
    client.post(login_url, {'username': 'testuser', 'password': 'password123'})

    # 3. The test visits the protected page (now logged in)
    products_url = reverse('catalog:list')
    response = client.get(products_url)

    # 4. Check that the page displays correctly
    assert response.status_code == 200
    assert "Visible Product" in response.content.decode()


@pytest.mark.django_db
def test_product_list_view_redirects_for_anonymous_user(client):
    """Checks that an anonymous visitor is redirected to the login page."""
    url = reverse('catalog:list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login'))