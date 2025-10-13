import pytest
from django.urls import reverse
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product
from inventory.models import Movement

@pytest.mark.django_db
def test_inventory_in_out_transfer_flow(client):
    """
    Teste le flux complet de soumission des formulaires d'entrée, sortie, et transfert.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company1 = Company.objects.create(name="Entreprise C1")
    company2 = Company.objects.create(name="Entreprise C2")
    product = Product.objects.create(name="Produit P1", sku="SKU1", company=company1, threshold=2)
    user = User.objects.create(
        username="test_user",
        password_hash=make_password("password123"),
        is_admin=True # On le met admin pour qu'il ait tous les droits
    )
    user.companies.add(company1, company2)

    # --- 2. Action : On se connecte en tant qu'utilisateur ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "test_user", "password": "password123"})

    # --- 3. Test du formulaire d'entrée (IN) ---
    stock_in_url = reverse('inventory:stock_in')
    response_in = client.post(stock_in_url, {
        "product_id": product.id,
        "company_id": company1.id,
        "quantity": 5,
        "note": "in"
    }, follow=True)
    assert response_in.status_code == 200

    # --- 4. Test du formulaire de sortie (OUT) ---
    stock_out_url = reverse('inventory:stock_out')
    response_out = client.post(stock_out_url, {
        "product_id": product.id,
        "company_id": company1.id,
        "quantity": 2,
        "note": "out"
    }, follow=True)
    assert response_out.status_code == 200

    # --- 5. Test du formulaire de transfert (TRANSFER) ---
    transfer_url = reverse('inventory:transfer')
    response_transfer = client.post(transfer_url, {
        "product_id": product.id,
        "quantity": 1,
        "company_from_id": company1.id,
        "company_to_id": company2.id,
        "note": "transfert"
    }, follow=True)
    assert response_transfer.status_code == 200

    # --- 6. Vérification finale : on visite la liste des mouvements ---
    list_url = reverse('inventory:list')
    response_list = client.get(list_url)
    html_content = response_list.content.decode()

    assert response_list.status_code == 200
    # On vérifie que les différents types de mouvements sont bien affichés
    assert "IN" in html_content
    assert "OUT" in html_content
    assert "TRANSFER" in html_content