from pathlib import Path
from django.conf import settings

def data_dir() -> Path:
    #  Ajoutons un petit helper centralisé pour récupérer le dossier data/.#
    # BASE_DIR pointe vers src/, on remonte d’un cran si nécessaire selon ton settings
    # Si ton BASE_DIR est déjà la racine du projet, garde simplement Path(settings.BASE_DIR) / "data"
    return Path(settings.BASE_DIR) / "data"
