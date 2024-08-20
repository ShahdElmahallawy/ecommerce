import pytest
from django.contrib.auth.models import User
from api.models import Wishlist, WishlistItem, Product
from api.services.wishlist import (
    add_item_to_wishlist,
    delete_item_from_wishlist,
    clear_wishlist,
)
from api.selectors.wishlist import get_wishlist_by_user


@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100.0, count=10)


@pytest.fixture
def wishlist(user):
    return get_wishlist_by_user(user)


@pytest.fixture
def wishlist_item(wishlist, product):
    return add_item_to_wishlist(wishlist, product)


def test_add_item_to_wishlist(wishlist, product):
    item = add_item_to_wishlist(wishlist, product)

    assert item.wishlist == wishlist
    assert item.product == product


def test_delete_item_from_wishlist(wishlist, wishlist_item):
    assert WishlistItem.objects.filter(id=wishlist_item.id).count() == 1

    result = delete_item_from_wishlist(wishlist, wishlist_item.product)

    assert result is True
    assert WishlistItem.objects.filter(id=wishlist_item.id).count() == 0


def test_clear_wishlist(wishlist, wishlist_item):
    clear_wishlist(wishlist)

    assert WishlistItem.objects.filter(wishlist=wishlist).count() == 0
