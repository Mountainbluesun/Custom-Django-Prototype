from typing import Optional
from .models import Product, Company

from .models import Product

def list_products():
    # Add select_related so company is loaded in memory
    return Product.objects.select_related('company').all()

def list_products_by_companies(company_ids):
    if not company_ids:
        return Product.objects.none()
    return Product.objects.filter(company_id__in=company_ids)


def get_product(product_id: int) -> Optional[Product]:
    """Retrieves a product by its ID."""
    return Product.objects.filter(id=product_id).first()

def create_product(name: str, sku: str, company_id: int, threshold: int = 0) -> Product:
    """Creates a new product."""
    # Get the Company object matching the ID
    company = Company.objects.get(id=company_id)
    new_product = Product.objects.create(
        name=name,
        sku=sku,
        company=company,
        threshold=threshold
    )
    return new_product

def update_product(product_id: int, data: dict) -> Optional[Product]:
    """Updates a product."""
    product = get_product(product_id)
    if product:
        product.name = data['name']
        product.sku = data['sku']
        product.company = Company.objects.get(id=data['company_id'])
        product.threshold = data.get('threshold', 0)
        product.save()
    return product

def delete_product(product_id: int) -> bool:
    """Deletes a product."""
    product = get_product(product_id)
    if product:
        product.delete()
        return True
    return False