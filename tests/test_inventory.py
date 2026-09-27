import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from inventory import service as inventory_service


@pytest.mark.django_db
def test_stock_computation():
    """
    Tests the full cycle of stock in, stock out, and stock computation for a product.
    """
    # --- 1. Setup: create the data in the test database ---
    company = Company.objects.create(name="Test Corp")
    product = Product.objects.create(name="Test Product", sku="SKU-TEST", company=company)

    # --- 2. Action: perform stock movements via the service ---

    # Add 15 units
    inventory_service.add_in(product_id=product.id, quantity=15, company_id=company.id)

    # Remove 5 units
    inventory_service.add_out(product_id=product.id, quantity=5, company_id=company.id)

    # Add 2 more units
    inventory_service.add_in(product_id=product.id, quantity=2, company_id=company.id)

    # --- 3. Verification ---

    # Check that all 3 movements were created in the database
    assert Movement.objects.count() == 3

    # Check that the final stock computation is correct (15 - 5 + 2 = 12)
    final_stock = inventory_service.compute_stock(product_id=product.id)
    assert final_stock == 12


@pytest.mark.django_db
def test_add_out_raises_error_on_insufficient_stock():
    """
    Checks that the add_out function raises an error when stock is insufficient.
    """
    company = Company.objects.create(name="Test Corp")
    product = Product.objects.create(name="Test Product", sku="SKU-TEST", company=company)

    # Put 10 units in stock
    inventory_service.add_in(product_id=product.id, quantity=10, company_id=company.id)

    # We expect the code to raise a ValueError
    # if we try to remove more than what's in stock (20 > 10)
    with pytest.raises(ValueError, match="Insufficient stock"):
        inventory_service.add_out(product_id=product.id, quantity=20, company_id=company.id)