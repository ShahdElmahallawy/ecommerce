import pytest
from api.models.cart import Cart
from api.models.cart_items import CartItems
from api.service.cart_service import (
    add_product_to_cart,
    remove_product_from_cart,
    calculate_cart_total,
    checkout_cart,
)
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category


@pytest.fixture
def user(db):
    return User.objects.create_user(
        username="testuser", email="test@example.com", password="password"
    )


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Test Product", price=100.00, count=10, category=category
    )


@pytest.fixture
def cart(user, db):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, product, db):
    return CartItems.objects.create(cart=cart, product_id=product, quantity=2)


def test_add_product_to_cart(user, product, db):
    cart = add_product_to_cart(user, product.id, 1)
    assert cart.cartitems_set.count() == 1
    assert cart.cartitems_set.first().product_id == product
    assert cart.cartitems_set.first().quantity == 1

    cart = add_product_to_cart(user, product.id, 2)
    assert cart.cartitems_set.first().quantity == 3


def test_remove_product_from_cart(user, cart_item, db):
    remove_product_from_cart(user, cart_item.product_id.id)
    assert cart_item.cart.cartitems_set.count() == 0


def test_calculate_cart_total(user, cart_item, db):
    total = calculate_cart_total(user)
    expected_total = cart_item.quantity * cart_item.product_id.price
    assert total == expected_total


def test_checkout_cart(user, cart_item, db):
    result = checkout_cart(user)
    assert result["status"] == "Checkout complete"
    assert result["total"] == cart_item.quantity * cart_item.product_id.price
