import pytest
from django.contrib.auth.models import User
from api.models import Wishlist, WishlistItem, Product
from api.selectors.wishlist import (
    get_wishlist_by_user,
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


def test_get_wishlist_item(user, wishlist_item):
    item = get_wishlist_item(user, wishlist_item.id)
    assert item == wishlist_item


def test_get_wishlist_item_fail(user, wishlist_item):
    with pytest.raises(WishlistItem.DoesNotExist):
        get_wishlist_item(user, 4)
