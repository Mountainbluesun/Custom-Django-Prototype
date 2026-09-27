# tests/utils.py
import sys
from pathlib import Path

# Add the src/ folder to PYTHONPATH for imports
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_PATH))

def test_utils_placeholder():
    """Minimal test to give coverage for the utils.py file"""
    assert SRC_PATH.exists()