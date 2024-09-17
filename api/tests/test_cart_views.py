import pytest
from api.models import Product
from django.urls import reverse
from rest_framework.exceptions import ValidationError


@pytest.fixture
def user_data():
    return {
        "email": "amr@example.com",
        "name": "Amr Test",
    }


@pytest.fixture
def product(db):
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_cart_view(user, api_client_auth):
    url = reverse("cart")
    response = api_client_auth.get(url)
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["items"] == []
    assert response.data["total_price"] == 0


@pytest.mark.django_db
def test_add_to_cart_view(user, api_client_auth, product):
    url = reverse("add-to-cart")
    data = {"product": product.id, "quantity": 1}
    response = api_client_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["user"] == user.id
    assert response.data["items"][0]["product"]["id"] == product.id
    assert response.data["items"][0]["quantity"] == 1
    assert response.data["total_price"] == 10

    response = api_client_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["user"] == user.id
    assert response.data["items"][0]["product"]["id"] == product.id
    assert response.data["items"][0]["quantity"] == 2
    assert response.data["total_price"] == 20


@pytest.mark.django_db
def test_add_to_cart_view_fail(user, api_client_auth, product):
    url = reverse("add-to-cart")
    data = {"product": product.id, "quantity": -1}

    response = api_client_auth.post(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_remove_from_cart_view(user, api_client_auth, product):
    url = reverse("remove-from-cart", args=[1])
    response = api_client_auth.delete(url)
    assert response.status_code == 400

    url = reverse("add-to-cart")
    data = {"product": product.id, "quantity": 1}
    response = api_client_auth.post(url, data)
    assert response.status_code == 201

    url = reverse("remove-from-cart", args=[1])
    response = api_client_auth.delete(url)
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["items"] == []
    assert response.data["total_price"] == 0


@pytest.mark.django_db
def test_clear_cart_view(user, api_client_auth, product):
    url = reverse("clear-cart")
    response = api_client_auth.delete(url)
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["items"] == []
    assert response.data["total_price"] == 0

    url = reverse("add-to-cart")
    data = {"product": product.id, "quantity": 1}
    response = api_client_auth.post(url, data)
    assert response.status_code == 201

    url = reverse("clear-cart")
    response = api_client_auth.delete(url)
    assert response.status_code == 200
    assert response.data["user"] == user.id
    assert response.data["items"] == []
    assert response.data["total_price"] == 0


def test_update_cart_item_view(user, api_client_auth, product):
    url = reverse("add-to-cart")
    data = {"product": product.id, "quantity": 1}
    response = api_client_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["items"][0]["product"]["id"] == product.id
    assert response.data["items"][0]["quantity"] == 1

    url = reverse("update-cart-item", args=[1])
    data = {"quantity": 5}
    response = api_client_auth.patch(url, data)
    assert response.status_code == 200
    assert response.data["items"][0]["product"]["id"] == product.id
    assert response.data["items"][0]["quantity"] == 5

    url = reverse("update-cart-item", args=[1])
    data = {"quantity": -1}
    response = api_client_auth.patch(url, data)
    assert response.status_code == 400
