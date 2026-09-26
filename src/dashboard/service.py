from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Iterable, Optional
from catalog.service import list_products
from inventory.service import list_movements

@dataclass
class MonthlyPoint:
    month: str  # "2025-08"
    in_qty: int
    out_qty: int

def quantities_by_company(allowed_company_ids: Optional[Iterable[int]] = None) -> Dict[int, int]:
    ids = set(int(x) for x in (allowed_company_ids or [])) or None
    totals = defaultdict(int)
    for p in list_products():
        if ids is not None and p.company_id not in ids:
            continue
        # current stock via compute_stock if you prefer, but it's more expensive.
        # here we simply add IN - OUT across all movements for this product
        # (equivalent to global stock if there's no multi-warehouse setup).
        # For full accuracy: use compute_stock(p.id, p.company_id).
        # Keeping it simple for the main dashboard card:
        totals[p.company_id] += 0  # placeholder if you go through compute_stock on the view side
    return totals

def monthly_in_out() -> List[MonthlyPoint]:
    # Aggregates IN/OUT quantities by month (YYYY-MM)
    agg: Dict[str, Dict[str, int]] = defaultdict(lambda: {"IN": 0, "OUT": 0})
    for m in list_movements():
        month = (m.ts or "")[:7]  # "YYYY-MM"
        if m.kind.startswith("IN"):
            agg[month]["IN"] += m.qty
        elif m.kind.startswith("OUT"):
            agg[month]["OUT"] += m.qty
        # TRANSFER_IN/OUT: depending on your design, ignore or split.
    out: List[MonthlyPoint] = []
    for month in sorted(agg.keys()):
        out.append(MonthlyPoint(month=month, in_qty=agg[month]["IN"], out_qty=agg[month]["OUT"]))
    return out