import io
import csv
import pytest
from src.catalog.csv_io import write_products_csv, read_products_csv

@pytest.mark.django_db
class DummyUploadedFile:
    """Simulates a minimal Django InMemoryUploadedFile."""
    def __init__(self, content: bytes):
        self.file = io.BytesIO(content)

@pytest.mark.django_db
def test_write_products_csv(tmp_path):
    """Tests that write_products_csv writes a correct CSV."""
    # Prepare a temporary file
    file_path = tmp_path / "products.csv"
    data = [
        {"name": "Product A", "sku": "A001", "company_id": 1, "threshold": 10},
        {"name": "Product B", "sku": "B002", "company_id": "2", "threshold": "5"},
        {"name": "Product C", "sku": "C003", "company_id": 3},  # no threshold
    ]

    with open(file_path, "w", newline="", encoding="utf-8") as fh:
        write_products_csv(fh, data)

    # Check the content
    with open(file_path, encoding="utf-8") as fh:
        reader = csv.DictReader(fh)
        rows = list(reader)

    assert rows[0] == {"name": "Product A", "sku": "A001", "company_id": "1", "threshold": "10"}
    assert rows[1] == {"name": "Product B", "sku": "B002", "company_id": "2", "threshold": "5"}
    assert rows[2] == {"name": "Product C", "sku": "C003", "company_id": "3", "threshold": "0"}  # default threshold

@pytest.mark.django_db
def test_read_products_csv_valid(tmp_path):
    """Tests that read_products_csv correctly reads a valid CSV."""
    csv_content = (
        "name;sku;company_id;threshold\n"
        "Product A;A001;1;10\n"
        "Product B;B002;2;\n"
    ).encode("utf-8")

    uploaded_file = DummyUploadedFile(csv_content)
    result = read_products_csv(uploaded_file)

    assert len(result) == 2
    assert result[0] == {"name": "Product A", "sku": "A001", "company_id": 1, "threshold": 10}
    assert result[1] == {"name": "Product B", "sku": "B002", "company_id": 2, "threshold": 0}

@pytest.mark.django_db
def test_read_products_csv_skips_incomplete(tmp_path):
    """Tests that read_products_csv skips incomplete rows."""
    csv_content = (
        "name;sku;company_id;threshold\n"
        "Product A;A001;1;10\n"
        ";B002;2;5\n"   # row with no name -> skipped
        "Product C;;3;7\n"  # row with no SKU -> skipped
        "Product D;D004;;3\n"  # row with no company_id -> skipped
    ).encode("utf-8")

    uploaded_file = DummyUploadedFile(csv_content)
    result = read_products_csv(uploaded_file)

    assert len(result) == 1
    assert result[0]["name"] == "Product A"