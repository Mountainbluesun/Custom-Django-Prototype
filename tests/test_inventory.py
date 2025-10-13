import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from inventory import service as inventory_service


@pytest.mark.django_db
def test_stock_computation():
    """
    Teste le cycle complet d'entrée, sortie, et calcul de stock pour un produit.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company = Company.objects.create(name="Test Corp")
    product = Product.objects.create(name="Produit Test", sku="SKU-TEST", company=company)

    # --- 2. Action : On fait des mouvements de stock via le service ---

    # On ajoute 15 unités
    inventory_service.add_in(product_id=product.id, quantity=15, company_id=company.id)

    # On retire 5 unités
    inventory_service.add_out(product_id=product.id, quantity=5, company_id=company.id)

    # On ajoute encore 2 unités
    inventory_service.add_in(product_id=product.id, quantity=2, company_id=company.id)

    # --- 3. Vérification ---

    # On vérifie que les 3 mouvements ont bien été créés dans la base de données
    assert Movement.objects.count() == 3

    # On vérifie que le calcul du stock final est correct (15 - 5 + 2 = 12)
    final_stock = inventory_service.compute_stock(product_id=product.id)
    assert final_stock == 12


@pytest.mark.django_db
def test_add_out_raises_error_on_insufficient_stock():
    """
    Vérifie que la fonction add_out lève une erreur si le stock est insuffisant.
    """
    company = Company.objects.create(name="Test Corp")
    product = Product.objects.create(name="Produit Test", sku="SKU-TEST", company=company)

    # On met 10 unités en stock
    inventory_service.add_in(product_id=product.id, quantity=10, company_id=company.id)

    # On s'attend à ce que le code lève une erreur ValueError
    # si on essaie de retirer plus que ce qu'il y a en stock (20 > 10)
    with pytest.raises(ValueError, match="Stock insuffisant"):
        inventory_service.add_out(product_id=product.id, quantity=20, company_id=company.id)