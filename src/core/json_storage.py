# src/core/json_storage.py
import json
from pathlib import Path
from threading import Lock
from typing import Any, Union

# Dossier "data" par défaut (prod/dev)
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LOCK = Lock()  # évite les accès concurrents

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def _resolve_path(filename_or_path: Union[str, Path], base_dir: Path) -> Path:
    """
    Accepte soit un nom de fichier (ex: 'users.json') soit un chemin absolu/relatif.
    Si c'est un nom, on le résout dans base_dir. Si c'est déjà un chemin, on le normalise.
    """
    p = Path(filename_or_path)
    return p if p.is_absolute() else (base_dir / p)

def load_json(filename_or_path: Union[str, Path], base_dir: Path = DATA_DIR) -> Any:
    """
    Charge du JSON depuis base_dir/filename (ou depuis un chemin complet si fourni).
    Retourne [] si le fichier n'existe pas.
    """
    filepath = _resolve_path(filename_or_path, base_dir)
    if not filepath.exists():
        return []
    with LOCK:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

def save_json(filename_or_path: Union[str, Path], data: Any, base_dir: Path = DATA_DIR) -> None:
    """
    Sauvegarde data au format JSON dans base_dir/filename (ou chemin complet).
    Écriture atomique: écrit d'abord *.tmp puis remplace.
    """
    filepath = _resolve_path(filename_or_path, base_dir)
    _ensure_dir(filepath.parent)
    tmp_path = filepath.with_suffix(filepath.suffix + ".tmp")
    with LOCK:
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path.replace(filepath)

