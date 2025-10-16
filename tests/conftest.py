# tests/conftest.py
import sys
from pathlib import Path
import pytest
from django.conf import settings

SRC = Path(__file__).resolve().parent.parent / "src"
sys.path.insert(0, str(SRC))

# NOTE: Cette fixture est NÉCESSAIRE pour les tests
# Les signed cookies (utilisés en prod) ne fonctionnent pas bien avec le client de test Django
# On force l'utilisation du backend DB pour les tests
@pytest.fixture(scope='session', autouse=True)
def django_db_setup(django_db_setup, django_db_blocker):
    """Override SESSION_ENGINE for tests to use database backend instead of signed cookies."""
    with django_db_blocker.unblock():
        # Change session backend to database for tests
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.db'
