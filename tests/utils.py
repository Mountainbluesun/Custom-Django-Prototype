# tests/utils.py
import sys
from pathlib import Path

# Ajouter le dossier src/ dans le PYTHONPATH pour les imports
SRC_PATH = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC_PATH))
