# src/catalog/csv_io.py
import csv
from io import TextIOWrapper
from typing import Iterable, List, Dict, IO

CSV_FIELDS = ["name", "sku", "company_id", "threshold"]

def write_products_csv(fh: IO[str], rows: Iterable[Dict]) -> None:
    """
    Writes products to CSV.
    rows: dicts with CSV_FIELDS keys (company_id, threshold as int).
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
    Reads an uploaded CSV (Django InMemoryUploadedFile / TemporaryUploadedFile).
    Returns a list of dicts ready for create_product / update_product.
    """
    # uploaded_file is binary -> TextIOWrapper in utf-8
    wrapper = TextIOWrapper(uploaded_file.file, encoding="utf-8")
    reader = csv.DictReader(wrapper)  # standard comma-separated CSV, like the export
    out: List[Dict] = []
    for row in reader:
        if not row.get("name") or not row.get("sku") or not row.get("company_id"):
            # skip incomplete rows
            continue
        out.append({
            "name": row["name"].strip(),
            "sku": row["sku"].strip(),
            "company_id": int(row["company_id"]),
            "threshold": int(row.get("threshold") or 0),
        })
    return out