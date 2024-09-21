import pytest
from api.services.store import create_store, update_store, delete_store
from api.tests.factories import StoreFactory, UserFactory
from api.models import Store


@pytest.fixture
def store(db):
    user = UserFactory(password=None, user_type="seller")
    store = StoreFactory(seller=user, is_default_shipping=True)
    return store


@pytest.mark.django_db
def test_create_store():
    user = UserFactory(password=None, user_type="seller")
    data = {
        "name": "My Store",
        "location": "123 Main St",
        "is_default_shipping": True,
    }
    store = create_store(user, data)
    assert store.name == data["name"]
    assert store.location == data["location"]
    assert store.is_default_shipping == data["is_default_shipping"]
    assert store.seller == user


def test_update_store(store):
    data = {
        "name": "My Store",
        "location": "123 Main St",
        "is_default_shipping": False,
    }
    updated_store = update_store(store, data)
    assert updated_store.name == data["name"]
    assert updated_store.location == data["location"]
    assert updated_store.is_default_shipping == data["is_default_shipping"]

    updated_store = update_store(store, {"name": "My Store"})
    assert updated_store.name == "My Store"
    assert updated_store.location == data["location"]


@pytest.mark.django_db
def test_delete_store(store):
    deleted_store = delete_store(store)
    assert deleted_store.is_deleted
    assert deleted_store in Store.objects.filter(is_deleted=True)
    assert deleted_store not in Store.objects.filter(is_deleted=False)
