import pytest
from companies.models import Company

@pytest.mark.django_db
def test_company_crud_database():
    """
    Tests CRUD for the Company model with the database.
    """
    # 1. READ (initial) - The database should be empty at the start
    assert Company.objects.count() == 0

    # 2. CREATE - Create a company
    company = Company.objects.create(name="Company A")
    assert Company.objects.count() == 1

    # 3. READ - Retrieve the company and check its name
    read_company = Company.objects.get(id=company.id)
    assert read_company.name == "Company A"

    # 4. UPDATE - Update the name
    read_company.name = "Company A+"
    read_company.save()

    # Check that the update was saved correctly
    updated_company = Company.objects.get(id=company.id)
    assert updated_company.name == "Company A+"

    # 5. DELETE - Delete the company
    updated_company.delete()
    assert Company.objects.count() == 0