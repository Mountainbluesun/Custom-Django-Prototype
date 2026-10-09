import re

import pytest
from captcha.models import CaptchaStore
from django.contrib.auth.hashers import make_password
from django.core import mail
from django.urls import reverse

from companies.models import Company
from users.models import User


def input_names(html):
    """Returns the names of all form fields found in the page."""
    names = re.findall(r'<(?:input|textarea)[^>]*\bname="([^"]+)"', html)
    return [name for name in names if name != "csrfmiddlewaretoken"]


@pytest.mark.django_db
def test_login_page_shows_login_and_contact_fields(client):
    """
    Checks that the login page shows both the login fields and the
    contact form fields (so visitors can actually type a message).
    """
    response = client.get(reverse("users:login"))

    assert response.status_code == 200
    names = input_names(response.content.decode())
    for expected in ["username", "password", "name", "email", "subject", "message", "captcha_1"]:
        assert expected in names


@pytest.mark.django_db
def test_wrong_password_shows_an_error_and_keeps_the_contact_form(client):
    """
    Checks that a failed login explains the problem to the visitor,
    and that the contact form is still displayed afterwards.
    """
    User.objects.create(username="admin", password=make_password("good-password"))

    response = client.post(reverse("users:login"), {"username": "admin", "password": "wrong"})

    html = response.content.decode()
    assert response.status_code == 200
    assert "Please enter a correct username and password" in html
    assert "message" in input_names(html)


@pytest.mark.django_db
def test_no_error_is_shown_on_a_fresh_login_page(client):
    """Checks that the error block stays hidden until a login fails."""
    response = client.get(reverse("users:login"))

    assert "Please enter a correct username and password" not in response.content.decode()


@pytest.mark.django_db
def test_contact_message_can_be_sent_from_the_login_page(client):
    """
    End-to-end check: fill in the contact form shown on the login page,
    solve its captcha, and make sure the email is sent.
    """
    html = client.get(reverse("users:login")).content.decode()
    captcha_key = re.search(r'name="captcha_0"[^>]*value="([^"]+)"', html) or re.search(
        r'value="([^"]+)"[^>]*name="captcha_0"', html
    )
    answer = CaptchaStore.objects.get(hashkey=captcha_key.group(1)).response

    response = client.post(
        reverse("contact"),
        {
            "name": "Visitor",
            "email": "visitor@example.com",
            "subject": "Hello",
            "message": "I have a project for you.",
            "captcha_0": captcha_key.group(1),
            "captcha_1": answer,
        },
        follow=True,
    )

    assert response.redirect_chain[-1][0] == reverse("users:login")
    assert "Your message has been sent successfully!" in response.content.decode()
    assert len(mail.outbox) == 1
    assert "Visitor" in mail.outbox[0].body


@pytest.mark.django_db
def test_confirmation_message_is_not_duplicated_on_other_pages(client):
    """
    Checks that a confirmation message is displayed only once
    (the layout used to render it twice).
    """
    User.objects.create(username="admin", password=make_password("pw12345"), is_admin=True)
    client.post(reverse("users:login"), {"username": "admin", "password": "pw12345"})

    response = client.post(reverse("companies:create"), {"name": "ACME"}, follow=True)

    assert Company.objects.filter(name="ACME").exists()
    assert response.content.decode().count("Company created.") == 1