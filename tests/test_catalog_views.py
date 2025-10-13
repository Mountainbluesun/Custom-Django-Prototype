import pytest
from django.urls import reverse
from companies.models import Company
from users.models import User
from catalog.models import Product
from django.contrib.auth.hashers import make_password


@pytest.mark.django_db
def test_product_list_view_for_logged_in_user(client):
    """Vérifie qu'un utilisateur qui se connecte peut voir les bons produits."""

    # 1. On prépare les données dans la base de test
    company1 = Company.objects.create(name="TestCorp 1")
    user = User.objects.create(
        username='testuser',
        password_hash=make_password('password123'),  # On utilise un mot de passe connu
        is_admin=True
    )
    user.companies.add(company1)
    Product.objects.create(name="Produit Visible", sku="A1", company=company1)

    # 2. Le test se connecte en utilisant votre vue de connexion
    login_url = reverse('users:login')
    client.post(login_url, {'username': 'testuser', 'password': 'password123'})

    # 3. Le test visite la page protégée (il est maintenant connecté)
    products_url = reverse('catalog:list')
    response = client.get(products_url)

    # 4. On vérifie que la page s'affiche correctement
    assert response.status_code == 200
    assert "Produit Visible" in response.content.decode()


@pytest.mark.django_db
def test_product_list_view_redirects_for_anonymous_user(client):
    """Vérifie qu'un visiteur anonyme est redirigé vers la page de connexion."""
    url = reverse('catalog:list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login'))