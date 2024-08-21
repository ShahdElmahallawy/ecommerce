import pytest
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from api.models import Product, Wishlist, WishlistItem
from api.serializers import (
    WishlistSerializer,
    WishlistItemSerializer,
    WishlistItemCreateSerializer,
)

from django.urls import reverse


@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100.0, count=10)


@pytest.fixture
def wishlist(user):
    return Wishlist.objects.create(user=user)


@pytest.fixture
def wishlist_item(wishlist, product):
    return WishlistItem.objects.create(wishlist=wishlist, product=product)


def test_wishlist_list_view(api_client_auth, wishlist):
    url = reverse("wishlist-list")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.data
    assert "user" in response.data


def test_wishlist_item_create_view(api_client_auth, product):
    data = {"product": product.id}
    url = reverse("wishlist-item-create")
    response = api_client_auth.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert "id" in response.data
    assert "product" in response.data


def test_wishlist_item_delete_view(api_client_auth, wishlist_item):
    url = reverse(
        "wishlist-item-delete", kwargs={"product_id": wishlist_item.product.id}
    )
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not WishlistItem.objects.filter(id=wishlist_item.id).exists()


def test_wishlist_delete_view(api_client_auth, wishlist, wishlist_item):
    url = reverse("wishlist-clear")
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert WishlistItem.objects.filter(wishlist=wishlist).count() == 0
