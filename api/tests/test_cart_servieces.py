import pytest
from api.models import CartItem, Product
from api.services.cart import (
    add_to_cart,
    remove_from_cart,
    clear_cart,
    update_cart_item,
)
from rest_framework.exceptions import ValidationError


@pytest.fixture
def product(db):
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_add_to_cart(user, product):
    cart = add_to_cart(user, product, 1)
    assert cart is not None
    assert cart.items.count() == 1

    cart_item = cart.items.first()
    assert cart_item.product == product
    assert cart_item.quantity == 1

    cart = add_to_cart(user, product, 2)
    assert cart.items.count() == 1
    cart_item = cart.items.first()
    assert cart_item.product == product
    assert cart_item.quantity == 3


@pytest.mark.django_db
def test_remove_from_cart(user, product):
    cart = add_to_cart(user, product, 1)
    assert cart.items.count() == 1

    cart = remove_from_cart(user, cart.items.first().id)
    assert cart.items.count() == 0


@pytest.mark.django_db
def test_remove_from_cart_invalid_item(user):
    with pytest.raises(ValidationError):
        remove_from_cart(user, 1)


@pytest.mark.django_db
def test_clear_cart(user, product):
    add_to_cart(user, product, 1)
    assert CartItem.objects.count() == 1

    cart = clear_cart(user)
    assert cart.items.count() == 0


@pytest.mark.django_db
def test_update_cart_item(user, product):
    cart = add_to_cart(user, product, 1)
    cart_item = cart.items.first()
    assert cart_item.quantity == 1

    cart = update_cart_item(user, cart_item.id, 5)
    cart_item = cart.items.first()
    assert cart_item.quantity == 5


@pytest.mark.django_db
def test_update_cart_item_invalid_item(user):
    with pytest.raises(ValidationError):
        update_cart_item(user, 1, 5)
