import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from alerts.service import compute_alerts


@pytest.mark.django_db
def test_compute_alerts_finds_products_under_threshold():
    """
    Checks that the compute_alerts service correctly identifies products on alert.
    """
    # --- 1. Setup: create the data in the test database ---
    company1 = Company.objects.create(name="Company 1")
    company2 = Company.objects.create(name="Company 2")

    # Product 1: Stock 8, Threshold 10 -> MUST be on alert
    p1 = Product.objects.create(name="Pen", sku="SKU1", company=company1, threshold=10)
    Movement.objects.create(product=p1, company=company1, quantity=8, kind='IN')

    # Product 2: Stock 5, Threshold 5 -> MUST be on alert (stock equal to threshold)
    p2 = Product.objects.create(name="Notebook", sku="SKU2", company=company1, threshold=5)
    Movement.objects.create(product=p2, company=company1, quantity=5, kind='IN')

    # Product 3: Stock 10, Threshold 7 -> MUST NOT be on alert
    p3 = Product.objects.create(name="Box", sku="SKU3", company=company2, threshold=7)
    Movement.objects.create(product=p3, company=company2, quantity=10, kind='IN')

    # --- 2. Action: call the service to compute the alerts ---
    # Compute across all companies
    all_company_ids = [company1.id, company2.id]
    alerts = compute_alerts(allowed_company_ids=all_company_ids)

    # --- 3. Verification ---
    # We expect 2 alerts: the pen and the notebook
    assert len(alerts) == 2

    # Check that the right products are in the alert list
    alert_product_names = {a.product_name for a in alerts}
    assert alert_product_names == {"Pen", "Notebook"}

    # We can even check the details of a specific alert
    pen_alert = next(a for a in alerts if a.product_name == "Pen")
    assert pen_alert.stock == 8
    assert pen_alert.threshold == 10