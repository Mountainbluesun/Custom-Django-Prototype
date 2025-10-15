import io
import csv
import pytest
from src.catalog.csv_io import write_products_csv, read_products_csv

@pytest.mark.django_db
class DummyUploadedFile:
    """Simule un Django InMemoryUploadedFile minimal."""
    def __init__(self, content: bytes):
        self.file = io.BytesIO(content)

@pytest.mark.django_db
def test_write_products_csv(tmp_path):
    """Teste que write_products_csv écrit un CSV correct."""
    # Prépare un fichier temporaire
    file_path = tmp_path / "products.csv"
    data = [
        {"name": "Produit A", "sku": "A001", "company_id": 1, "threshold": 10},
        {"name": "Produit B", "sku": "B002", "company_id": "2", "threshold": "5"},
        {"name": "Produit C", "sku": "C003", "company_id": 3},  # sans threshold
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as fh:
        write_products_csv(fh, data)

    # Vérifie le contenu
    with open(file_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    assert rows[0] == {"name": "Produit A", "sku": "A001", "company_id": "1", "threshold": "10"}
    assert rows[1] == {"name": "Produit B", "sku": "B002", "company_id": "2", "threshold": "5"}
    assert rows[2] == {"name": "Produit C", "sku": "C003", "company_id": "3", "threshold": "0"}  # threshold par défaut

@pytest.mark.django_db
def test_read_products_csv_valid(tmp_path):
    """Teste que read_products_csv lit correctement un CSV valide."""
    csv_content = (
        "name;sku;company_id;threshold\n"
        "Produit A;A001;1;10\n"
        "Produit B;B002;2;\n"
    ).encode("utf-8")

    uploaded_file = DummyUploadedFile(csv_content)
    result = read_products_csv(uploaded_file)

    assert len(result) == 2
    assert result[0] == {"name": "Produit A", "sku": "A001", "company_id": 1, "threshold": 10}
    assert result[1] == {"name": "Produit B", "sku": "B002", "company_id": 2, "threshold": 0}

@pytest.mark.django_db
def test_read_products_csv_skips_incomplete(tmp_path):
    """Teste que read_products_csv ignore les lignes incomplètes."""
    csv_content = (
        "name;sku;company_id;threshold\n"
        "Produit A;A001;1;10\n"
        ";B002;2;5\n"   # ligne sans nom -> ignorée
        "Produit C;;3;7\n"  # ligne sans SKU -> ignorée
        "Produit D;D004;;3\n"  # ligne sans company_id -> ignorée
    ).encode("utf-8")

    uploaded_file = DummyUploadedFile(csv_content)
    result = read_products_csv(uploaded_file)

    assert len(result) == 1
    assert result[0]["name"] == "Produit A"
