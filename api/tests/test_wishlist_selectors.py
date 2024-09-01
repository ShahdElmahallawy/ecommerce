import pytest
from django.contrib.auth.models import User
from api.models import Wishlist, WishlistItem, Product, Category
from api.selectors.wishlist import (
    get_wishlist_by_user,
    get_wishlist_item,
)


@pytest.fixture
def category():
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(category):
    return Product.objects.create(
        name="Test Product", price=100.0, count=10, category=category
    )


@pytest.fixture
def wishlist(user):
    return get_wishlist_by_user(user)


@pytest.fixture
def wishlist_item(wishlist, product):
    return WishlistItem.objects.create(wishlist=wishlist, product=product)


def test_get_wishlist_by_user(user):
    wishlist = get_wishlist_by_user(user)
    assert wishlist.user == user


def test_get_wishlist_item(wishlist, wishlist_item):
    item = get_wishlist_item(wishlist, wishlist_item.id)
    assert item == wishlist_item


def test_get_wishlist_item_fail(wishlist, wishlist_item):
    with pytest.raises(WishlistItem.DoesNotExist):
        get_wishlist_item(wishlist, 4)
