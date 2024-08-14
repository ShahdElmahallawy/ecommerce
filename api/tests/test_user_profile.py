import pytest
from django.urls import reverse
from rest_framework import status

from api.models import Profile

@pytest.mark.django_db
def test_retrieve_profile(api_client_auth, user):
    url = reverse('user-profile')
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['user']['email'] == user.email
    assert response.data['address'] == user.profile.address

@pytest.mark.django_db
def test_update_profile(api_client_auth, user):
    url = reverse('user-profile')
    data = {
        "user": {
            "name": "Amr New"
        },
        "address": "Cairo",
        "phone": "01234567890",
        "preferred_currency": "EGP"
    }
    response = api_client_auth.patch(url, data, format='json')
    assert response.status_code == status.HTTP_200_OK
    user.profile.refresh_from_db()
    assert user.name == "Amr New"
    assert user.profile.address == "Cairo"
    assert user.profile.phone == "01234567890"
    assert user.profile.preferred_currency == "EGP"

@pytest.mark.django_db
def test_create_profile_signal(user):
    assert Profile.objects.filter(user=user).exists()
