# src/alerts/service.py
from dataclasses import dataclass
from typing import Iterable, List, Optional

from catalog.service import list_products, list_products_by_companies
from inventory.service import compute_stock




@dataclass

class AlertItem:
    product_id: int
    product_name: str
    company_id: int
    threshold: int
    stock: int





def compute_alerts(allowed_company_ids: Optional[Iterable[int]] = None) -> List[AlertItem]:
    # Utilise list_products_by_companies pour filtrer dès la requête SQL
    if allowed_company_ids is not None:
        ids = list(int(x) for x in allowed_company_ids)
        products = list_products_by_companies(ids)
    else:
        products = list_products()

    alerts: List[AlertItem] = []
    for p in products:
        stock = compute_stock(p.id)
        if stock <= p.threshold:
            alerts.append(AlertItem(
                product_id=p.id,
                product_name=p.name,
                company_id=p.company_id,
                threshold=p.threshold,
                stock=stock,
            )
        )
    return alerts