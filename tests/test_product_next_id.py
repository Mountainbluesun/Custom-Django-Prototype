import pytest
from catalog.models import Product
from companies.models import Company

@pytest.mark.django_db
def test_product_crud_database():
    """
    Teste le cycle complet (CRUD) pour le modèle Product avec la base de données.
    """
    # --- Préparation : On a besoin d'une entreprise pour y lier le produit ---
    company = Company.objects.create(name="Entreprise Test")

    # 1. Vérification initiale : La table des produits doit être vide
    assert Product.objects.count() == 0

    # 2. CREATE : On crée un produit
    Product.objects.create(
        name="Produit A",
        sku="SKU-A",
        company=company,
        threshold=10
    )
    assert Product.objects.count() == 1

    # 3. READ : On récupère le produit et on vérifie ses attributs
    product = Product.objects.first()
    assert product is not None
    assert product.name == "Produit A"
    assert product.company.name == "Entreprise Test"

    # 4. UPDATE : On met à jour le produit
    product.name = "Produit A modifié"
    product.save()

    # On recharge le produit depuis la base de données pour être sûr
    product.refresh_from_db()
    assert product.name == "Produit A modifié"

    # 5. DELETE : On supprime le produit
    product.delete()
    assert Product.objects.count() == 0