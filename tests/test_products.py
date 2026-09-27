import pytest
from catalog.models import Product
from companies.models import Company


@pytest.mark.django_db
def test_product_crud_and_filters_database():
    """
    Tests the full CRUD cycle and filtering for the Product model
    with the database.
    """
    # --- Setup: we need companies to link the products to ---
    company1 = Company.objects.create(name="Company 1")
    company2 = Company.objects.create(name="Company 2")

    # 1. READ (initial) - The product table should be empty
    assert Product.objects.count() == 0

    # 2. CREATE - Create three products
    Product.objects.create(name="Pen", sku="SKU-PEN", company=company1, threshold=10)
    Product.objects.create(name="Notebook", sku="SKU-NOTEBOOK", company=company1, threshold=5)
    Product.objects.create(name="Box", sku="SKU-BOX", company=company2, threshold=7)
    assert Product.objects.count() == 3

    # 3. READ - Retrieve a product and check its name
    pen = Product.objects.get(name="Pen")
    assert pen.sku == "SKU-PEN"

    # 4. UPDATE - Update the notebook's threshold
    notebook = Product.objects.get(name="Notebook")
    notebook.threshold = 12
    notebook.save()

    # Reload from the database to make sure
    notebook.refresh_from_db()
    assert notebook.threshold == 12

    # 5. DELETE - Delete the box
    box = Product.objects.get(name="Box")
    box.delete()
    assert Product.objects.count() == 2

    # 6. FILTER - Only retrieve products from the first company
    company1_products = Product.objects.filter(company=company1)
    assert company1_products.count() == 2

    # Check that the names are correct
    product_names = {p.name for p in company1_products}
    assert product_names == {"Pen", "Notebook"}