import pytest
from catalog.models import Product
from companies.models import Company

@pytest.mark.django_db
def test_product_crud_database():
    """
    Tests the full CRUD cycle for the Product model with the database.
    """
    # --- Setup: we need a company to link the product to ---
    company = Company.objects.create(name="Test Company")

    # 1. Initial check: the product table should be empty
    assert Product.objects.count() == 0

    # 2. CREATE: create a product
    Product.objects.create(
        name="Product A",
        sku="SKU-A",
        company=company,
        threshold=10
    )
    assert Product.objects.count() == 1

    # 3. READ: retrieve the product and check its attributes
    product = Product.objects.first()
    assert product is not None
    assert product.name == "Product A"
    assert product.company.name == "Test Company"

    # 4. UPDATE: update the product
    product.name = "Product A modified"
    product.save()

    # Reload the product from the database to make sure
    product.refresh_from_db()
    assert product.name == "Product A modified"

    # 5. DELETE: delete the product
    product.delete()
    assert Product.objects.count() == 0