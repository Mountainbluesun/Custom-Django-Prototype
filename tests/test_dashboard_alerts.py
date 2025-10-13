import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_dashboard_alerts_view(client):
    """Teste que la page du tableau de bord des alertes s'affiche bien."""
    url = reverse("dashboard:index")  # <-- ajuste ici si ton nom de vue est différent
    response = client.get(url)

    assert response.status_code == 200
    assert b"Dashboard" in response.content
    assert b"Produits en alerte" in response.content
