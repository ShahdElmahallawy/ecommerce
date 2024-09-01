from rest_framework.exceptions import ValidationError
import pytest
from api.models import WishlistItem, Product, Category
from api.services.wishlist import (
    add_item_to_wishlist,
    delete_item_from_wishlist,
    clear_wishlist,
)
from api.selectors.wishlist import get_wishlist_by_user


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
    return add_item_to_wishlist(wishlist, product)


def test_add_item_to_wishlist(wishlist, product):
    wishlist = add_item_to_wishlist(wishlist, product)

    assert wishlist.user == wishlist.user
    assert wishlist.items.count() == 1
    assert wishlist.items.first().product == product


def test_add_item_to_wishlist_item_exists(wishlist, product):
    wishlist = add_item_to_wishlist(wishlist, product)
    assert wishlist.items.count() == 1

    with pytest.raises(ValidationError):
        wishlist = add_item_to_wishlist(wishlist, product)


def test_delete_item_from_wishlist(wishlist, wishlist_item):
    assert wishlist.items.count() == 1

    wishlist = delete_item_from_wishlist(wishlist, wishlist_item.id)

    assert wishlist.items.count() == 0


def test_delete_item_from_wishlist_fail(wishlist, wishlist_item):
    assert wishlist.items.count() == 1

    with pytest.raises(ValidationError):
        delete_item_from_wishlist(wishlist, 4)


def test_clear_wishlist(wishlist, wishlist_item):
    clear_wishlist(wishlist)

    assert WishlistItem.objects.filter(wishlist=wishlist).count() == 0
