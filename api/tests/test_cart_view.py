import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.cart import Cart
from api.models.product import Product
from api.models.cart_items import CartItems
from rest_framework import status
from api.views.cart_view import CartView
from api.serializers.cart_serializer import CartSerializer
from api.service.cart_service import add_product_to_cart, remove_product_from_cart, calculate_cart_total, checkout_cart
from unittest.mock import patch

@pytest.mark.django_db
def test_add_product_to_cart():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    assert cart.cartitems_set.count() == 1
    assert cart.cartitems_set.first().product == product
    assert cart.cartitems_set.first().quantity == 1

@pytest.mark.django_db
def test_remove_product_from_cart():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    remove_product_from_cart(user, product.id)
    assert cart.cartitems_set.count() == 0

@pytest.mark.django_db
def test_calculate_cart_total():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    total = calculate_cart_total(user)
    assert total == 10

@pytest.mark.django_db
def test_checkout_cart():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    response = checkout_cart(user)
    assert response == {'success': True}

@pytest.mark.django_db
def test_cart_view_create():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(reverse('cart-list'), {'product_id': product.id, 'quantity': 1})
    assert response.status_code == status.HTTP_201_CREATED
    assert CartItems.objects.count() == 1
    assert CartItems.objects.first().product == product
    assert CartItems.objects.first().quantity == 1

@pytest.mark.django_db
def test_cart_view_destroy():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.delete(reverse('cart-detail', args=[product.id]))
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert CartItems.objects.count() == 0

@pytest.mark.django_db
def test_cart_view_list():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('cart-list'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == CartSerializer(cart).data

@pytest.mark.django_db
def test_cart_view_total_price():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get(reverse('cart-total-price'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'total': 10}

@pytest.mark.django_db
def test_cart_view_checkout():
    user = User.objects.create_user(username='test', password='test')
    product = Product.objects.create(name='test', price=10)
    cart = add_product_to_cart(user, product.id, 1)
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.post(reverse('cart-checkout'))
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {'success': True}

