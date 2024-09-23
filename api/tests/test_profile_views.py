import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from api.models import Profile
from api.models.address import Address


@pytest.mark.django_db
def test_retrieve_profile(api_client_auth, user):
    url = reverse("profile-detail")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["user"]["email"] == user.email


@pytest.mark.django_db
def test_retrieve_profile_not_found(api_client_auth, user):
    Profile.objects.filter(user=user).delete()
    url = reverse("profile-detail")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_profile(api_client_auth, user):
    url = reverse("profile-update")
    address = Address.objects.create(
        user=user,
        street_address="123 Paymob St",
        apartment_address="Apt 1",
        country="EGP",
        zip=12345,
        address_type="company",
    )
    data = {
        "user": {"name": "Amr New"},
        "address": address.id,
        "phone": "01234567890",
        "preferred_currency": "EGP",
    }
    response = api_client_auth.patch(url, data, format="json")
    user = get_user_model().objects.get(id=user.id)
    profile = user.profile

    assert response.status_code == status.HTTP_200_OK
    assert user.name == "Amr New"
    update = profile.address
    assert update.street_address == "123 Paymob St"
    assert update.apartment_address == "Apt 1"
    assert update.country == "EGP"
    assert update.zip == 12345
    assert update.address_type == "company"
    assert user.profile.phone == "01234567890"
    assert user.profile.preferred_currency == "EGP"


@pytest.mark.django_db
def test_update_profile_not_found(api_client_auth, user):
    Profile.objects.filter(user=user).delete()
    url = reverse("profile-update")
    data = {
        "user": {"name": "Amr New"},
        "address": "Cairo",
        "phone": "01234567890",
        "preferred_currency": "EGP",
    }
    response = api_client_auth.patch(url, data, format="json")
    user = get_user_model().objects.get(id=user.id)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_update_profile_invalid_phone(api_client_auth, user):
    # not 11 digits
    url = reverse("profile-update")
    data = {
        "phone": "123",
    }
    response = api_client_auth.patch(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_profile_signal(user):
    assert Profile.objects.filter(user=user).exists()
