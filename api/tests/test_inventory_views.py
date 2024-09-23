import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.selectors.inventory import (
    get_inventory_by_id,
    get_inventory_by_id_and_seller,
    get_inventory_by_seller,
)
from api.services.inventory import create_inventory, update_inventory, delete_inventory

from api.tests.factories import (
    InventoryFactory,
    ProductFactory,
    StoreFactory,
    UserFactory,
)


@pytest.fixture
def inventory(db):
    user = UserFactory(password=None, user_type="seller")
    product = ProductFactory(created_by=user, image=None)
    store = StoreFactory(seller=user, is_default_shipping=True)
    inventory = InventoryFactory(product=product, store=store)
    client = APIClient()
    client.force_authenticate(user=user)
    return inventory, client


def test_inventory_list_view(inventory):
    inventory, client = inventory
    url = reverse("inventory-list")
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["id"] == inventory.id


@pytest.mark.django_db
def test_inventory_create_view():
    user = UserFactory(password=None, user_type="seller")
    product = ProductFactory(created_by=user, image=None)
    store = StoreFactory(seller=user, is_default_shipping=True)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("inventory-create")
    data = {"product": product.id, "store": store.id, "stock": 10}
    response = client.post(url, data)
    print(response.data)
    assert response.status_code == 201
    assert response.data["product"]["id"] == product.id
    assert response.data["store"] == store.id
    assert response.data["stock"] == 10


@pytest.mark.django_db
def test_inventory_create_view_invalid():
    user = UserFactory(password=None, user_type="seller")
    product = ProductFactory(created_by=user, image=None)
    store = StoreFactory(seller=user, is_default_shipping=True)
    client = APIClient()
    client.force_authenticate(user=user)
    url = reverse("inventory-create")

    # invalid stock
    data = {"product": product.id, "store": store.id, "stock": -10}
    response = client.post(url, data)
    assert response.status_code == 400

    # no product
    data = {"store": store.id, "stock": 10}
    response = client.post(url, data)
    assert response.status_code == 400

    # invalid product
    data = {"product": 100, "store": store.id, "stock": 10}
    response = client.post(url, data)
    assert response.status_code == 400

    user2 = UserFactory(password=None, user_type="seller")
    client2 = APIClient()
    client2.force_authenticate(user=user2)
    data = {"product": product.id, "store": store.id, "stock": 10}
    response = client2.post(url, data)
    assert response.status_code == 400

    # invalid store
    data = {"product": product.id, "store": 100, "stock": 10}
    response = client.post(url, data)
    assert response.status_code == 400


def test_inventory_retrieve_view(inventory):
    inventory, client = inventory
    url = reverse("inventory-detail", kwargs={"inventory_id": inventory.id})
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == inventory.id

    # not found
    url = reverse("inventory-detail", kwargs={"inventory_id": 100})
    response = client.get(url)
    assert response.status_code == 404


def test_inventory_update_view(inventory):
    inventory, client = inventory
    url = reverse("inventory-update", kwargs={"inventory_id": inventory.id})
    data = {"stock": 20}
    response = client.patch(url, data)
    assert response.status_code == 200
    assert response.data["stock"] == 20

    user2 = UserFactory(password=None, user_type="seller")
    client2 = APIClient()
    client2.force_authenticate(user=user2)
    response = client2.patch(url, data)
    assert response.status_code == 404


def test_inventory_delete_view(inventory):
    inventory, client = inventory
    url = reverse("inventory-delete", kwargs={"inventory_id": inventory.id})
    response = client.delete(url)
    assert response.status_code == 204
    assert get_inventory_by_id(inventory.id) is None

    response = client.delete(url)
    assert response.status_code == 404
