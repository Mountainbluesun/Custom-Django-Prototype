# Fichier : src/companies/service.py
from typing import List, Optional



from .models import Company

# companies/service.py
def list_companies(company_ids=None):
    """Retourne la liste des entreprises accessibles selon les IDs autorisés."""
    if company_ids is None:
        return Company.objects.all()
    if not company_ids:
        return Company.objects.none()
    return Company.objects.filter(id__in=company_ids)




def create_company(name: str, owner: Optional[str] = None) -> Company:
    """Crée une nouvelle entreprise dans la base de données."""
    new_company = Company.objects.create(name=name, owner=owner)
    return new_company

def get_company(company_id: int) -> Optional[Company]:
    """Récupère une entreprise par son ID."""
    return Company.objects.filter(id=company_id).first()

def update_company(company_id: int, name: str, owner: Optional[str] = None) -> Optional[Company]:
    """Met à jour une entreprise."""
    company = get_company(company_id)
    if company:
        company.name = name
        company.owner = owner
        company.save()
    return company

def delete_company(company_id: int) -> bool:
    """Supprime une entreprise."""
    company = get_company(company_id)
    if company:
        company.delete()
        return True
    return False