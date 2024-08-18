import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.cart import Cart
from api.models.product import Product
from api.models.cart_items import CartItems
from rest_framework import status
from api.views.cart_view import CartView

# from api.serializers.cart_serializer import CartSerializer
from api.service.cart_service import (
    add_product_to_cart,
    remove_product_from_cart,
    calculate_cart_total,
    checkout_cart,
)

# from unittest.mock import patch


@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username="test", password="test")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def create_product():
    return Product.objects.create(name="test", price=10)


@pytest.fixture
def create_cart():
    return Cart.objects.create(
        user=User.objects.create_user(username="test", password="test")
    )


@pytest.fixture
def create_cart_item(create_cart, create_product):
    return CartItems.objects.create(
        cart=create_cart, product=create_product, quantity=1
    )


def test_add_product_to_cart(create_cart, create_product):
    cart = add_product_to_cart(create_cart.user, create_product.id, 1)
    assert cart.cartitems_set.count() == 1
    assert cart.cartitems_set.first().product == create_product
    assert cart.cartitems_set.first().quantity == 1


def test_remove_product_from_cart(create_cart_item):
    remove_product_from_cart(create_cart_item.cart.user, create_cart_item.product.id)
    assert create_cart_item.cart.cartitems_set.count() == 0


def test_calculate_cart_total(create_cart_item):
    total = calculate_cart_total(create_cart_item.cart.user)
    assert total == 10


def test_checkout_cart(create_cart_item):
    response = checkout_cart(create_cart_item.cart.user)
    assert response == {"success": True}
