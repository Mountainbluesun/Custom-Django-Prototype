import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from inventory import service as inventory_service

@pytest.mark.django_db
def test_stock_computation_and_transfer():
    """
    Tests the full cycle of stock in, stock out, transfer and stock computation.
    """
    # --- 1. Setup: create the data in the test database ---
    company_a = Company.objects.create(name="Company A")
    company_b = Company.objects.create(name="Company B")
    product = Product.objects.create(name="Test Product", sku="SKU-TEST", company=company_a)

    # --- 2. Action and Verification ---

    # IN 10 -> Stock A = 10
    inventory_service.add_in(product_id=product.id, quantity=10, company_id=company_a.id)
    assert inventory_service.compute_stock(product_id=product.id) == 10

    # OUT 3 -> Stock A = 7
    inventory_service.add_out(product_id=product.id, quantity=3, company_id=company_a.id)
    assert inventory_service.compute_stock(product_id=product.id) == 7

    # TRANSFER 2 from A to B -> Stock A = 5, Stock B (implicit) = 2
    # Note: Your `compute_stock` computes the product's total stock, across all companies.
    # For a more precise test, a function computing stock per company would be needed.
    # But we can check the total.
    inventory_service.add_transfer(
        product_id=product.id,
        quantity=2,
        company_from_id=company_a.id,
        company_to_id=company_b.id
    )
    # The product's total stock is still 7 (5 at A, 2 at B)
    assert inventory_service.compute_stock(product_id=product.id) == 7


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
    with pytest.raises(ValueError):
        inventory_service.add_out(product_id=product.id, quantity=20, company_id=company.id)