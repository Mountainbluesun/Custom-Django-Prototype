import pytest
from django.urls import reverse



# tests/test_dashboard_alerts.py
import pytest
from django.urls import reverse



def test_dashboard_alerts_view(client):
    url = reverse("dashboard:view")
    response = client.get(url)
    assert response.status_code == 200
    assert b"Dashboard" in response.content
    assert b"Produits en alerte" in response.content