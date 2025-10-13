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
        # stock courant via compute_stock si tu préfères, mais ça coûte plus cher.
        # ici on additionne simplement IN - OUT sur tous mouvements pour ce produit
        # (équivalent au stock global si pas de multi-entrepôt).
        # Si tu veux la rigueur: utilise compute_stock(p.id, p.company_id).
        # On reste simple pour la carte principale :
        totals[p.company_id] += 0  # placeholder si tu passes par compute_stock côté vue
    return totals

def monthly_in_out() -> List[MonthlyPoint]:
    # Agrège par mois (YYYY-MM) les quantités IN/OUT
    agg: Dict[str, Dict[str, int]] = defaultdict(lambda: {"IN": 0, "OUT": 0})
    for m in list_movements():
        month = (m.ts or "")[:7]  # "YYYY-MM"
        if m.kind.startswith("IN"):
            agg[month]["IN"] += m.qty
        elif m.kind.startswith("OUT"):
            agg[month]["OUT"] += m.qty
        # TRANSFER_IN/OUT : selon ta vision, ignore ou répartis.
    out: List[MonthlyPoint] = []
    for month in sorted(agg.keys()):
        out.append(MonthlyPoint(month=month, in_qty=agg[month]["IN"], out_qty=agg[month]["OUT"]))
    return out
