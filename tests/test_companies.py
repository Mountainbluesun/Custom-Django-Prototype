import pytest
from companies.models import Company

@pytest.mark.django_db
def test_company_crud_database():
    """
    Teste le CRUD pour le modèle Company avec la base de données.
    """
    # 1. READ (initial) - La base de données doit être vide au début
    assert Company.objects.count() == 0

    # 2. CREATE - On crée une entreprise
    company = Company.objects.create(name="Entreprise A")
    assert Company.objects.count() == 1

    # 3. READ - On récupère l'entreprise et on vérifie son nom
    read_company = Company.objects.get(id=company.id)
    assert read_company.name == "Entreprise A"

    # 4. UPDATE - On met à jour le nom
    read_company.name = "Entreprise A+"
    read_company.save()

    # On vérifie que la mise à jour a bien été enregistrée
    updated_company = Company.objects.get(id=company.id)
    assert updated_company.name == "Entreprise A+"

    # 5. DELETE - On supprime l'entreprise
    updated_company.delete()
    assert Company.objects.count() == 0