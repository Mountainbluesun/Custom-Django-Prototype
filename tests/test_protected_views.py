# Working pytest version
from django.urls import reverse


# No need for @pytest.mark.django_db since we don't touch the database
def test_alerts_view_redirects_anonymous_user(client):
    """
    Checks that an anonymous visitor is redirected from the alerts page.
    """
    url = reverse('alerts:list')
    response = client.get(url)

    assert response.status_code == 302
    assert response.url.startswith(reverse('users:login'))