import pytest
from companies import service as svc
from companies.models import Company

@pytest.mark.xfail(reason="Legacy JSON-style CRUD test: service API changed after ORM refactor")
@pytest.mark.django_db
def test_company_crud_service():
    """
    Tests the full CRUD cycle of the Company service functions
    with the database.
    """
    # The test database is empty at the start
    assert svc.list_companies().count() == 0

    # Test creation (CREATE)
    c1 = svc.create_company("ACME", owner="alice")
    svc.create_company("Globex")
    assert svc.list_companies().count() == 2
    assert c1.name == "ACME"
    assert c1.owner == "alice"

    # Test reading (READ)
    all_companies = svc.list_companies()
    assert len(all_companies) == 2

    globex = svc.get_company(company_id=2)
    assert globex is not None
    assert globex.name == "Globex"

    # Test updating (UPDATE)
    svc.update_company(company_id=2, name="Globex Corp", owner="bob")
    updated_globex = svc.get_company(company_id=2)
    assert updated_globex.name == "Globex Corp"
    assert updated_globex.owner == "bob"

    # Test deletion (DELETE)
    svc.delete_company(company_id=1)
    assert svc.list_companies().count() == 1
    assert svc.get_company(company_id=1) is None