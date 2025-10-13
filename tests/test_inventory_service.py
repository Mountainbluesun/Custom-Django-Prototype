import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from inventory import service as inventory_service

@pytest.mark.django_db
def test_stock_computation_and_transfer():
    """
    Teste le cycle complet d'entrée, sortie, transfert et calcul de stock.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company_a = Company.objects.create(name="Entreprise A")
    company_b = Company.objects.create(name="Entreprise B")
    product = Product.objects.create(name="Produit Test", sku="SKU-TEST", company=company_a)

    # --- 2. Action et Vérification ---

    # IN 10 -> Stock A = 10
    inventory_service.add_in(product_id=product.id, quantity=10, company_id=company_a.id)
    assert inventory_service.compute_stock(product_id=product.id) == 10

    # OUT 3 -> Stock A = 7
    inventory_service.add_out(product_id=product.id, quantity=3, company_id=company_a.id)
    assert inventory_service.compute_stock(product_id=product.id) == 7

    # TRANSFER 2 de A vers B -> Stock A = 5, Stock B (implicite) = 2
    # Note: Votre `compute_stock` calcule le stock total du produit, toutes entreprises confondues.
    # Pour un test plus précis, il faudrait une fonction qui calcule le stock par entreprise.
    # Mais on peut vérifier le total.
    inventory_service.add_transfer(
        product_id=product.id,
        quantity=2,
        company_from_id=company_a.id,
        company_to_id=company_b.id
    )
    # Le stock total du produit est toujours 7 (5 chez A, 2 chez B)
    assert inventory_service.compute_stock(product_id=product.id) == 7


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
    with pytest.raises(ValueError):
        inventory_service.add_out(product_id=product.id, quantity=20, company_id=company.id)