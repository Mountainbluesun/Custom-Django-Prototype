import pytest
from django.urls import reverse


# Pas besoin de @pytest.mark.django_db car ce test ne touche pas à la base de données.
def test_protected_view_redirects_anonymous_user(client):
    """
    Vérifie qu'un visiteur anonyme est bien redirigé depuis une page protégée.
    """
    # On récupère l'URL de la page des alertes de manière dynamique
    url = reverse('alerts:list')

    # On visite la page
    response = client.get(url)

    # On vérifie qu'on est bien redirigé (code 302)
    assert response.status_code == 302
    # On vérifie que la redirection pointe bien vers la page de connexion
    assert response.url.startswith(reverse('users:login'))