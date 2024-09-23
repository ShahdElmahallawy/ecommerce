import pytest
from api.models import Inventory
from api.selectors.inventory import (
    get_inventory_by_id,
    get_inventory_by_id_and_seller,
    get_inventory_by_seller,
)
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


def test_get_inventory_by_id(inventory):
    inventory_id = inventory.id
    assert get_inventory_by_id(inventory_id) == inventory


def test_get_inventory_by_id_and_seller(inventory):
    seller = inventory.product.created_by
    inventory_id = inventory.id
    assert get_inventory_by_id_and_seller(inventory_id, seller) == inventory

    user2 = UserFactory(password=None, user_type="seller")
    assert get_inventory_by_id_and_seller(inventory_id, user2) is None


def test_get_inventory_by_seller(inventory):
    seller = inventory.product.created_by
    assert get_inventory_by_seller(seller).count() == 1

    user2 = UserFactory(password=None, user_type="seller")
    assert get_inventory_by_seller(user2).count() == 0
