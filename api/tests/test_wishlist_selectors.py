import pytest
from django.contrib.auth.models import User
from api.models import Wishlist, WishlistItem, Product
from api.selectors.wishlist import (
    get_wishlist_by_user,
    get_wishlist_items,
    get_wishlist_item,
)


@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100.0, count=10)


@pytest.fixture
def wishlist(user):
    return get_wishlist_by_user(user)


@pytest.fixture
def wishlist_item(wishlist, product):
    return WishlistItem.objects.create(wishlist=wishlist, product=product)


def test_get_wishlist_by_user(user):
    wishlist = get_wishlist_by_user(user)

    assert wishlist.user == user


def test_get_wishlist_items(wishlist, wishlist_item):
    items = get_wishlist_items(wishlist)

    assert items.count() == 1
    assert items.first() == wishlist_item


def test_get_wishlist_item(wishlist, product, wishlist_item):
    item = get_wishlist_item(wishlist, product)

    assert item == wishlist_item
