# File: src/companies/service.py
from typing import List, Optional
from .models import Company

# companies/service.py
def list_companies(company_ids=None):
    """Returns the list of companies accessible for the given allowed IDs."""
    if company_ids is None:
        return Company.objects.all()
    if not company_ids:
        return Company.objects.none()
    return Company.objects.filter(id__in=company_ids)




def create_company(name: str, owner: Optional[str] = None) -> Company:
    """Creates a new company in the database."""
    new_company = Company.objects.create(name=name, owner=owner)
    return new_company

def get_company(company_id: int) -> Optional[Company]:
    """Retrieves a company by its ID."""
    return Company.objects.filter(id=company_id).first()

def update_company(company_id: int, name: str, owner: Optional[str] = None) -> Optional[Company]:
    """Updates a company."""
    company = get_company(company_id)
    if company:
        company.name = name
        company.owner = owner
        company.save()
    return company

def delete_company(company_id: int) -> bool:
    """Deletes a company."""
    company = get_company(company_id)
    if company:
        company.delete()
        return True
    return False