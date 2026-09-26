# src/core/json_storage.py
import json
from pathlib import Path
from threading import Lock
from typing import Any, Union

# Default "data" folder (prod/dev)
DATA_DIR = Path(__file__).resolve().parent.parent.parent / "data"
LOCK = Lock()  # prevents concurrent access

def _ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)

def _resolve_path(filename_or_path: Union[str, Path], base_dir: Path) -> Path:
    """
    Accepts either a filename (e.g. 'users.json') or an absolute/relative path.
    If it's a name, resolve it within base_dir. If it's already a path, normalize it.
    """
    p = Path(filename_or_path)
    return p if p.is_absolute() else (base_dir / p)

def load_json(filename_or_path: Union[str, Path], base_dir: Path = DATA_DIR) -> Any:
    """
    Loads JSON from base_dir/filename (or from a full path if provided).
    Returns [] if the file does not exist.
    """
    filepath = _resolve_path(filename_or_path, base_dir)
    if not filepath.exists():
        return []
    with LOCK:
        with filepath.open("r", encoding="utf-8") as f:
            return json.load(f)

def save_json(filename_or_path: Union[str, Path], data: Any, base_dir: Path = DATA_DIR) -> None:
    """
    Saves data as JSON to base_dir/filename (or a full path).
    Atomic write: writes to *.tmp first, then replaces.
    """
    filepath = _resolve_path(filename_or_path, base_dir)
    _ensure_dir(filepath.parent)
    tmp_path = filepath.with_suffix(filepath.suffix + ".tmp")
    with LOCK:
        with tmp_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        tmp_path.replace(filepath)