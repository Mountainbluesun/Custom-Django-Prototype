# Version pytest fonctionnelle
import pytest
from django.urls import reverse


# Pas besoin de @pytest.mark.django_db car on ne touche pas à la base de données
def test_alerts_view_redirects_anonymous_user(client):
    """
    Vérifie qu'un visiteur anonyme est redirigé depuis la page des alertes.
    """
    url = reverse('alerts:list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login'))