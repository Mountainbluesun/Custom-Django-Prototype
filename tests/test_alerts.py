import pytest
from companies.models import Company
from catalog.models import Product
from inventory.models import Movement
from alerts.service import compute_alerts


@pytest.mark.django_db
def test_compute_alerts_finds_products_under_threshold():
    """
    Vérifie que le service compute_alerts identifie correctement les produits en alerte.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company1 = Company.objects.create(name="Entreprise 1")
    company2 = Company.objects.create(name="Entreprise 2")

    # Produit 1 : Stock 8, Seuil 10 -> DOIT être en alerte
    p1 = Product.objects.create(name="Stylo", sku="SKU1", company=company1, threshold=10)
    Movement.objects.create(product=p1, company=company1, quantity=8, kind='IN')

    # Produit 2 : Stock 5, Seuil 5 -> DOIT être en alerte (stock égal au seuil)
    p2 = Product.objects.create(name="Cahier", sku="SKU2", company=company1, threshold=5)
    Movement.objects.create(product=p2, company=company1, quantity=5, kind='IN')

    # Produit 3 : Stock 10, Seuil 7 -> NE DOIT PAS être en alerte
    p3 = Product.objects.create(name="Carton", sku="SKU3", company=company2, threshold=7)
    Movement.objects.create(product=p3, company=company2, quantity=10, kind='IN')

    # --- 2. Action : On appelle le service pour calculer les alertes ---
    # On calcule pour toutes les entreprises
    all_company_ids = [company1.id, company2.id]
    alerts = compute_alerts(allowed_company_ids=all_company_ids)

    # --- 3. Vérification ---
    # On s'attend à 2 alertes : le stylo et le cahier
    assert len(alerts) == 2

    # On vérifie que les bons produits sont dans la liste des alertes
    alert_product_names = {a.product_name for a in alerts}
    assert alert_product_names == {"Stylo", "Cahier"}

    # On peut même vérifier les détails d'une alerte spécifique
    stylo_alert = next(a for a in alerts if a.product_name == "Stylo")
    assert stylo_alert.stock == 8
    assert stylo_alert.threshold == 10