import pytest
from django.urls import reverse
from users.models import User
from django.contrib.auth.hashers import make_password
from bs4 import BeautifulSoup

@pytest.mark.django_db
def test_successful_login(client):
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_active=True
    )

    url = reverse("users:login")
    resp = client.post(url, {
        "username": "testuser",
        "password": "password123"
    }, follow=True)

    assert resp.status_code == 200

    soup = BeautifulSoup(resp.content, "html.parser")
    success_alert = soup.select_one(".alert-success")
    assert success_alert is not None or "Bienvenue" in resp.content.decode()


@pytest.mark.django_db
def test_failed_login_with_wrong_password(client):
    User.objects.create(
        username="testuser",
        password=make_password("password123"),
        is_active=True
    )

    url = reverse("users:login")
    resp = client.post(url, {
        "username": "testuser",
        "password": "WRONGPASS"
    }, follow=True)

    assert resp.status_code == 200

    assert (
        "Veuillez entrer des identifiants valides" in resp.content.decode()
        or "identifiants invalides" in resp.content.decode()
    )

    soup = BeautifulSoup(resp.content, "html.parser")
    assert soup.select_one(".messages") is not None

