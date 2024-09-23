import pytest

from api.selectors.store import (
    get_store_by_id,
    get_store_by_seller,
    get_stores_by_seller,
    get_default_shipping_store,
    get_stores,
    get_stock_in_default_store,
)
from api.tests.factories import (
    StoreFactory,
    UserFactory,
    ProductFactory,
    InventoryFactory,
)


@pytest.fixture
def store(db):
    user = UserFactory(password=None, user_type="seller")
    store = StoreFactory(seller=user, is_default_shipping=True)
    return store


def test_get_stores(store):
    assert get_stores().count() == 1

    store2 = StoreFactory(seller=store.seller)
    assert get_stores().count() == 2


def test_get_store_by_id(store):
    store_id = store.id
    assert get_store_by_id(store_id) == store

    # not found
    assert get_store_by_id(100) is None


def test_get_store_by_seller(store):
    seller = store.seller
    store_id = store.id
    assert get_store_by_seller(seller, store_id) == store

    user2 = UserFactory(password=None, user_type="seller")
    assert get_store_by_seller(user2, store_id) is None


def test_get_stores_by_seller(store):
    seller = store.seller
    assert get_stores_by_seller(seller).count() == 1

    user2 = UserFactory(password=None, user_type="seller")
    assert get_stores_by_seller(user2).count() == 0


def test_get_default_shipping_store(store):
    seller = store.seller
    assert get_default_shipping_store(seller) == store

    store.is_default_shipping = False
    store.save()
    assert get_default_shipping_store(seller) is None

    store2 = StoreFactory(seller=seller, is_default_shipping=True)
    assert get_default_shipping_store(seller) == store2


def test_get_stock_in_default_store(store):
    product = ProductFactory(created_by=None, category=None, image=None)
    assert get_stock_in_default_store(product) == 0

    InventoryFactory(store=store, product=product, stock=10)

    assert get_stock_in_default_store(store.inventory.first().product) == 10
