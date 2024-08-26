import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.cart import Cart
from api.models.product import Product
from api.models.cart_items import CartItems
from decimal import Decimal
from api.models.category import Category
from api.service.cart_service import (
    add_product_to_cart,
    remove_product_from_cart,
    calculate_cart_total,
    checkout_cart,
)

@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username="test", password="test")
    client = APIClient()
    client.force_authenticate(user=user)

    return client
@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def create_product(db, category):
    return Product.objects.create(
        name="test",
        price=Decimal('10.00'),
        description="Sample description",
        count=1,
        currency='USD',
        category=category,
    )

@pytest.fixture
def create_cart(authenticated_client):
    user = authenticated_client.handler._force_user
    return Cart.objects.create(user=user)

@pytest.fixture
def create_cart_item(create_cart, create_product):
    return CartItems.objects.create(
        cart=create_cart, product_id=create_product, quantity=1
    )

@pytest.mark.django_db
def test_add_product_to_cart(create_cart, create_product):
    cart = add_product_to_cart(create_cart.user, create_product.id, 1)
    assert cart.cartitems_set.count() == 1
    assert cart.cartitems_set.first().product_id.id == create_product.id
    # assert cart.cartitems_set.first().product_id == create_product.id
    assert cart.cartitems_set.first().quantity == 1

@pytest.mark.django_db
def test_remove_product_from_cart(create_cart_item):
    remove_product_from_cart(create_cart_item.cart.user, create_cart_item.product_id.id)
    assert create_cart_item.cart.cartitems_set.count() == 0

@pytest.mark.django_db
def test_calculate_cart_total(create_cart_item):
    total = calculate_cart_total(create_cart_item.cart.user)
    assert total == Decimal('10.00')

@pytest.mark.django_db
def test_checkout_cart(create_cart_item):
    response = checkout_cart(create_cart_item.cart.user)
    expected_response = {'status': 'Checkout complete', 'total': Decimal('10.00')}
    assert response == expected_response
