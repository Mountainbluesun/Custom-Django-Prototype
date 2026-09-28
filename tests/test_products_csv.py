import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product

@pytest.mark.django_db
def test_export_and_import_products_csv(client):
    """
    Tests the full flow of exporting then importing products via CSV.
    """
    # --- 1. Setup: create the data in the test database ---
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")

    Product.objects.create(name="Product P1", sku="SKU1", company=company1, threshold=2)

    admin_user = User.objects.create(
        username="admin",
        password=make_password("password123"),
        is_admin=True
    )
    admin_user.companies.add(company1, company2)

    # --- 2. Action: log in as admin ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin", "password": "password123"})

    # --- 3. Test the EXPORT ---
    export_url = reverse('catalog:export_csv')
    response_export = client.get(export_url)

    # Check the export
    assert response_export.status_code == 200
    assert response_export['Content-Type'] == 'text/csv'
    csv_content = response_export.content.decode('utf-8')
    assert "name,sku,company_id,threshold" in csv_content
    assert f"Product P1,SKU1,{company1.id},2" in csv_content

    # --- 4. Test the IMPORT ---
    # Prepare a new CSV file to import
    csv_to_import = f"name,sku,company_id,threshold\nNew Product,SKU2,{company2.id},5"
    uploaded_file = SimpleUploadedFile(
        "import.csv",
        csv_to_import.encode("utf-8"),
        content_type="text/csv"
    )

    import_url = reverse('catalog:import_csv')
    client.post(import_url, {"csv_file": uploaded_file})

    # --- 5. Check the import ---
    # Check that the new product was correctly created in the database
    assert Product.objects.count() == 2
    new_product = Product.objects.get(sku="SKU2")
    assert new_product.name == "New Product"
    assert new_product.company.id == company2.id
    assert new_product.threshold == 5


@pytest.mark.django_db
def test_import_warns_when_no_valid_rows(client):
    """
    Checks that importing a file with no readable row (for example a
    semicolon-separated file) shows a warning instead of a silent success.
    """
    admin_user = User.objects.create(
        username="admin",
        password=make_password("password123"),
        is_admin=True
    )
    company = Company.objects.create(name="ACME")
    admin_user.companies.add(company)

    client.post(reverse('users:login'), {"username": "admin", "password": "password123"})

    semicolon_csv = f"name;sku;company_id;threshold\nSemicolon Product;SKU9;{company.id};5"
    uploaded_file = SimpleUploadedFile(
        "import.csv",
        semicolon_csv.encode("utf-8"),
        content_type="text/csv"
    )
    response = client.post(reverse('catalog:import_csv'), {"csv_file": uploaded_file}, follow=True)

    assert "No valid rows found" in response.content.decode()
    assert Product.objects.count() == 0