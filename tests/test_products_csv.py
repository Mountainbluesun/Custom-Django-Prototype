import pytest
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth.hashers import make_password
from companies.models import Company
from users.models import User
from catalog.models import Product


@pytest.mark.django_db
def test_export_and_import_products_csv(client):
    """
    Teste le flux complet d'exportation puis d'importation de produits via CSV.
    """
    # --- 1. Préparation : On crée les données dans la base de données de test ---
    company1 = Company.objects.create(name="ACME")
    company2 = Company.objects.create(name="Globex")

    Product.objects.create(name="Produit P1", sku="SKU1", company=company1, threshold=2)

    admin_user = User.objects.create(
        username="admin",
        password_hash=make_password("password123"),
        is_admin=True
    )
    admin_user.companies.add(company1, company2)

    # --- 2. Action : On se connecte en tant qu'admin ---
    login_url = reverse('users:login')
    client.post(login_url, {"username": "admin", "password": "password123"})

    # --- 3. Test de l'EXPORT ---
    export_url = reverse('catalog:export_csv')
    response_export = client.get(export_url)

    # Vérification de l'export
    assert response_export.status_code == 200
    assert response_export['Content-Type'] == 'text/csv'
    csv_content = response_export.content.decode('utf-8')
    assert "name,sku,company_id,threshold" in csv_content
    assert "Produit P1,SKU1,1,2" in csv_content

    # --- 4. Test de l'IMPORT ---
    # On prépare un nouveau fichier CSV à importer
    csv_to_import = "name;sku;company_id;threshold\nNouveau Produit;SKU2;2;5"
    uploaded_file = SimpleUploadedFile(
        "import.csv",
        csv_to_import.encode("utf-8"),
        content_type="text/csv"
    )

    import_url = reverse('catalog:import_csv')
    client.post(import_url, {"csv_file": uploaded_file})

    # --- 5. Vérification de l'import ---
    # On vérifie que le nouveau produit a bien été créé dans la base de données
    assert Product.objects.count() == 2
    new_product = Product.objects.get(sku="SKU2")
    assert new_product.name == "Nouveau Produit"
    assert new_product.company.id == company2.id
    assert new_product.threshold == 5