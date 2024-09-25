import pytest
from django.urls import reverse
from api.tests.factories import StoreFactory, UserFactory
from rest_framework.test import APIClient


@pytest.fixture
def store(db):
    user = UserFactory(password=None, user_type="seller")
    store = StoreFactory(seller=user, is_default_shipping=True)
    return store


def test_list_store_view(client, store):
    url = reverse("store-list")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_store_detail_view(client, store):
    url = reverse("store-detail", args=[store.id])
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()["id"] == store.id


def test_store_by_seller_view(store):
    client = APIClient()
    client.force_authenticate(user=store.seller)
    url = reverse("store-by-seller")
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) == 1

    user2 = UserFactory(password=None, user_type="seller")
    client.force_authenticate(user=user2)
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.json()) == 0


def test_store_create_view(client, store):
    client = APIClient()
    client.force_authenticate(user=store.seller)
    url = reverse("store-create")
    data = {
        "name": "My Store",
        "location": "123 Main St",
        "is_default_shipping": True,
    }
    response = client.post(url, data=data)
    assert response.status_code == 201
    assert response.json()["name"] == data["name"]
    assert response.json()["location"] == data["location"]
    assert response.json()["is_default_shipping"] == data["is_default_shipping"]
    assert response.json()["seller"] == store.seller.id


def test_store_update_view(client, store):
    client = APIClient()
    client.force_authenticate(user=store.seller)
    url = reverse("store-update", args=[store.id])
    data = {
        "name": "My Store",
        "location": "123 Main St",
        "is_default_shipping": False,
    }
    response = client.patch(url, data=data)
    assert response.status_code == 200
    assert response.json()["name"] == data["name"]
    assert response.json()["location"] == data["location"]
    assert response.json()["is_default_shipping"] == data["is_default_shipping"]

    response = client.patch(url, data={"name": "My Store"})
    assert response.status_code == 200
    assert response.json()["name"] == "My Store"
    assert response.json()["location"] == data["location"]

    url = reverse("store-update", args=[store.id + 1])
    response = client.patch(url, data=data)
    assert response.status_code == 404


def test_store_delete_view(client, store):
    client = APIClient()
    client.force_authenticate(user=store.seller)
    url = reverse("store-delete", args=[store.id])
    response = client.delete(url)
    assert response.status_code == 204

    response = client.delete(url)
    assert response.status_code == 404

    url = reverse("store-delete", args=[store.id + 1])
    response = client.delete(url)
    assert response.status_code == 404
