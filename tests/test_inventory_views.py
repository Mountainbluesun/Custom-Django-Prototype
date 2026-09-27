import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement

@pytest.mark.django_db
def test_inventory_in_out_transfer_flow(client):
    """
    Tests the full submission flow of the stock-in, stock-out, and transfer forms.
    """
    # --- 1. Setup: create the data in the test database ---
    company1 = Company.objects.create(name="Company C1")
    company2 = Company.objects.create(name="Company C2")
    product = Product.objects.create(name="Product P1", sku="SKU1", company=company1, threshold=2)
    user = User.objects.create(
        username="test_user",
        password=make_password("password123"),
        is_admin=True # Made admin so they have all the necessary permissions
    )
    user.companies.add(company1, company2)

    # --- 2. Action: log in as the user ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "test_user", "password": "password123"})

    # --- 3. Test the stock-in form (IN) ---
    stock_in_url = reverse('inventory:stock_in')
    response_in = client.post(stock_in_url, {
        "product_id": product.id,
        "company_id": company1.id,
        "quantity": 5,
        "note": "in"
    }, follow=True)
    assert response_in.status_code == 200

    # --- 4. Test the stock-out form (OUT) ---
    stock_out_url = reverse('inventory:stock_out')
    response_out = client.post(stock_out_url, {
        "product_id": product.id,
        "company_id": company1.id,
        "quantity": 2,
        "note": "out"
    }, follow=True)
    assert response_out.status_code == 200

    # --- 5. Test the transfer form (TRANSFER) ---
    transfer_url = reverse('inventory:transfer')
    response_transfer = client.post(transfer_url, {
        "product_id": product.id,
        "quantity": 1,
        "company_from_id": company1.id,
        "company_to_id": company2.id,
        "note": "transfer"
    }, follow=True)
    assert response_transfer.status_code == 200

    # --- 6. Final check: visit the movements list ---
    list_url = reverse('inventory:list')
    response_list = client.get(list_url)
    html_content = response_list.content.decode()

    assert response_list.status_code == 200
    # Check that the different movement types are correctly displayed
    assert "IN" in html_content
    assert "OUT" in html_content
    assert "TRANSFER" in html_content