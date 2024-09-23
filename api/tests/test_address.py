import pytest
from rest_framework import status
from api.tests.factories import AddressFactory
from django.urls import reverse


@pytest.fixture
def address(user):
    return AddressFactory(user=user)


@pytest.mark.django_db
def test_address_list(api_client_auth, address):
    url = reverse("address_list")
    response = api_client_auth.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1
    assert response.data[0]["street_address"] == address.street_address


@pytest.mark.django_db
def test_address_detail(api_client_auth, address):
    url = reverse("address_detail", kwargs={"pk": address.pk})
    response = api_client_auth.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["street_address"] == address.street_address


@pytest.mark.django_db
def test_address_update(api_client_auth, address, user):
    url = reverse("address_update", kwargs={"pk": address.pk})
    data = {
        "street_address": "123 paymob St",
        "apartment_address": "Apt 20B",
        "country": "EG",
        "zip": 30303,
        "address_type": "work",
    }
    response = api_client_auth.patch(url, data, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["street_address"] == "123 paymob St"


@pytest.mark.django_db
def test_address_delete(api_client_auth, address):
    url = reverse("address_delete", kwargs={"pk": address.pk})
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
