from pathlib import Path
from django.conf import settings

def data_dir() -> Path:
    #  Let's add a small centralized helper to get the data/ folder.#
    # BASE_DIR points to src/, go up one level if needed depending on your settings
    # If your BASE_DIR is already the project root, just keep Path(settings.BASE_DIR) / "data"
    return Path(settings.BASE_DIR) / "data"