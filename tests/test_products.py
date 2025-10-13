import pytest
from catalog.models import Product
from companies.models import Company


@pytest.mark.django_db
def test_product_crud_and_filters_database():
    """
    Teste le cycle complet (CRUD) et le filtrage pour le modèle Product
    avec la base de données.
    """
    # --- Préparation : On a besoin d'entreprises pour y lier les produits ---
    company1 = Company.objects.create(name="Entreprise 1")
    company2 = Company.objects.create(name="Entreprise 2")

    # 1. READ (initial) - La table des produits doit être vide
    assert Product.objects.count() == 0

    # 2. CREATE - On crée trois produits
    Product.objects.create(name="Stylo", sku="SKU-STYLO", company=company1, threshold=10)
    Product.objects.create(name="Cahier", sku="SKU-CAHIER", company=company1, threshold=5)
    Product.objects.create(name="Carton", sku="SKU-CARTON", company=company2, threshold=7)
    assert Product.objects.count() == 3

    # 3. READ - On récupère un produit et on vérifie son nom
    stylo = Product.objects.get(name="Stylo")
    assert stylo.sku == "SKU-STYLO"

    # 4. UPDATE - On met à jour le seuil du cahier
    cahier = Product.objects.get(name="Cahier")
    cahier.threshold = 12
    cahier.save()

    # On recharge depuis la base de données pour être sûr
    cahier.refresh_from_db()
    assert cahier.threshold == 12

    # 5. DELETE - On supprime le carton
    carton = Product.objects.get(name="Carton")
    carton.delete()
    assert Product.objects.count() == 2

    # 6. FILTER - On ne récupère que les produits de la première entreprise
    company1_products = Product.objects.filter(company=company1)
    assert company1_products.count() == 2

    # On vérifie que les noms sont corrects
    product_names = {p.name for p in company1_products}
    assert product_names == {"Stylo", "Cahier"}