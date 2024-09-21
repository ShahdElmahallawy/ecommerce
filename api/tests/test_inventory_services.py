import pytest
from api.services.inventory import create_inventory, update_inventory, delete_inventory
from api.models import Inventory
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
    return inventory


@pytest.mark.django_db
def test_create_inventory():
    user = UserFactory(password=None, user_type="seller")
    product = ProductFactory(created_by=user, image=None)
    store = StoreFactory(seller=user, is_default_shipping=True)
    stock = 10
    new_inventory = create_inventory(
        user, {"product": product.id, "store": store.id, "stock": stock}
    )
    assert new_inventory.product == product
    assert new_inventory.store == store
    assert new_inventory.stock == stock


def test_update_inventory(inventory):
    new_stock = 20
    updated_inventory = update_inventory(inventory, {"stock": new_stock})
    assert updated_inventory.stock == new_stock


def test_delete_inventory(inventory):
    inventory_id = inventory.id
    delete_inventory(inventory)
    assert Inventory.objects.filter(id=inventory_id).count() == 0
