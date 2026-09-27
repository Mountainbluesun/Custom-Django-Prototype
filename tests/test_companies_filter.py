import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User

@pytest.mark.django_db
def test_company_list_is_filtered_by_user_scope(client):
    """
    Checks that a non-admin user only sees the companies
    they are assigned to.
    """
    # --- 1. Setup: create the data in the test database ---

    # Create two companies
    company_acme = Company.objects.create(name="ACME")
    company_globex = Company.objects.create(name="Globex")

    # Create a non-admin user and assign them only to Globex
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company_globex)

    # --- 2. Action: log in as the restricted user ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 3. Action: visit the company list page ---
    companies_url = reverse('companies:list')
    response = client.get(companies_url)

    # --- 4. Verification ---
    assert response.status_code == 200
    html_content = response.content.decode()

    # The user should see the company assigned to them (Globex)
    assert "Globex" in html_content
    # The user should NOT see the other company (ACME)
    assert "ACME" not in html_content