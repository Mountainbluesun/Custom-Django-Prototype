# src/alerts/service.py
from dataclasses import dataclass
from typing import Iterable, List, Optional

from catalog.service import list_products
from inventory.service import compute_stock

from dataclasses import dataclass

from typing import Iterable, List, Optional




@dataclass

class AlertItem:
    product_id: int
    product_name: str
    company_id: int
    threshold: int
    stock: int





def compute_alerts(allowed_company_ids: Optional[Iterable[int]] = None) -> List[AlertItem]:
    ids = set(int(x) for x in (allowed_company_ids or [])) or None
    alerts: List[AlertItem] = []
    for p in list_products():
        if ids is not None and p.company_id not in ids: continue
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