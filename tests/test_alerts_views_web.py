import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password

from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement


@pytest.mark.django_db
@pytest.mark.xfail(reason="User-company scoping not implemented yet")
def test_alerts_user_scoped(client):
    """
    Vérifie qu'un utilisateur non-admin voit uniquement les alertes
    des entreprises auxquelles il a accès.
    """
    # --- 1. Création des entreprises ---
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")

    # --- 2. Création d'un utilisateur non-admin ---
    user = User.objects.create(
        username="user_scoped",
        password=make_password("password123"),
        is_admin=False
    )
    user.companies.add(company1)

    # --- 3. Création des produits ---
    product1 = Product.objects.create(name="Produit ACME", sku="P1", company=company1, threshold=5)
    product2 = Product.objects.create(name="Produit Globex", sku="P2", company=company2, threshold=5)

    # --- 4. Création des mouvements (alerte) ---
    Movement.objects.create(product=product1, company=company1, quantity=1, kind='IN')
    Movement.objects.create(product=product2, company=company2, quantity=2, kind='IN')

    # --- 5. Connexion de l'utilisateur ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_scoped", "password": "password123"})

    # --- 6. Accès à la page des alertes ---
    alerts_url = reverse('alerts:list')
    response = client.get(alerts_url)
    assert response.status_code == 200
    html_content = response.content.decode()

    # --- 7. Vérification du contenu ---
    assert "Produit ACME" in html_content
    assert "Produit Globex" not in html_content


@pytest.mark.django_db
def test_alerts_admin_sees_all(client):
    """
    Vérifie qu'un utilisateur admin voit toutes les alertes,
    peu importe l'entreprise.
    """
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")
    admin = User.objects.create(username="admin", password=make_password("admin123"), is_admin=True)

    product1 = Product.objects.create(name="Produit ACME", sku="P1", company=company1, threshold=5)
    product2 = Product.objects.create(name="Produit Globex", sku="P2", company=company2, threshold=5)

    Movement.objects.create(product=product1, company=company1, quantity=1, kind='IN')
    Movement.objects.create(product=product2, company=company2, quantity=1, kind='IN')

    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin", "password": "admin123"})

    response = client.get(reverse('alerts:list'))
    assert response.status_code == 200
    html_content = response.content.decode()
    assert "Produit ACME" in html_content
    assert "Produit Globex" in html_content


@pytest.mark.django_db
def test_alerts_no_products(client):
    """
    Vérifie le comportement lorsque aucune alerte n'existe.
    """
    user = User.objects.create(username="user_empty", password=make_password("password123"), is_admin=False)
    login_url = reverse('users:login')
    client.post(login_url, {"username": "user_empty", "password": "password123"})

    response = client.get(reverse('alerts:list'))
    assert response.status_code == 200
    html_content = response.content.decode()
    # Pas d'alertes affichées
    assert "Aucune alerte." in html_content

