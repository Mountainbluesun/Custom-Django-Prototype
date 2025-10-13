# src/catalog/csv_io.py
import csv
from io import TextIOWrapper
from typing import Iterable, List, Dict, IO

CSV_FIELDS = ["name", "sku", "company_id", "threshold"]

def write_products_csv(fh: IO[str], rows: Iterable[Dict]) -> None:
    """
    Écrit les produits en CSV.
    rows: dicts avec clés CSV_FIELDS (company_id, threshold en int).
    """
    writer = csv.DictWriter(fh, fieldnames=CSV_FIELDS)
    writer.writeheader()
    for r in rows:
        writer.writerow({
            "name": r["name"],
            "sku": r["sku"],
            "company_id": int(r["company_id"]),
            "threshold": int(r.get("threshold", 0)),
        })

def read_products_csv(uploaded_file) -> List[Dict]:
    """
    Lit un CSV uploadé (Django InMemoryUploadedFile / TemporaryUploadedFile).
    Retourne une liste de dicts prêts pour create_product / update_product.
    """
    # uploaded_file est binaire -> TextIOWrapper en utf-8
    wrapper = TextIOWrapper(uploaded_file.file, encoding="utf-8")
    reader = csv.DictReader(wrapper, delimiter= ";")
    out: List[Dict] = []
    for row in reader:
        if not row.get("name") or not row.get("sku") or not row.get("company_id"):
            # on ignore lignes incomplètes
            continue
        out.append({
            "name": row["name"].strip(),
            "sku": row["sku"].strip(),
            "company_id": int(row["company_id"]),
            "threshold": int(row.get("threshold") or 0),
        })
    return out
