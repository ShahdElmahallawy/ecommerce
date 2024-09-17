from unittest.mock import patch
import os
from django.urls import reverse
from rest_framework import status
import pytest
from rest_framework.test import APIClient
from api.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def product(user):
    return Product.objects.create(name="Product", price=10, count=10, created_by=user)


@pytest.mark.django_db
def test_product_list_view(api_client, product):
    url = reverse("product-list")
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data[0]["name"] == "Product"
    assert response.data[0]["price"] == 10


@pytest.mark.django_db
def test_product_detail_view(api_client, product):
    url = reverse("product-detail", args=[product.id])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Product"
    assert response.data["price"] == 10


@pytest.mark.django_db
def test_product_detail_view_not_found(api_client):
    url = reverse("product-detail", args=[1])
    response = api_client.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_product_create_view_not_admin_nor_seller(api_client_auth):
    url = reverse("product-create")
    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
    }

    response = api_client_auth.post(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
@patch("django.db.models.fields.files.ImageFieldFile.save", return_value=None)
@patch("django.db.models.fields.files.ImageFieldFile.delete", return_value=None)
def test_product_create_view_admin(mock_save, mock_delete, api_admin_auth):
    mock_save.return_value = None
    image_path = os.path.join(os.path.dirname(__file__), "test_files", "test_image.png")

    image_mock = SimpleUploadedFile(
        name="test_image.jpg",
        content=open(image_path, "rb").read(),
        content_type="image/jpeg",
    )

    url = reverse("product-create")

    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
        "currency": "USD",
        "image": image_mock,
    }
    response = api_admin_auth.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Product"
    assert response.data["price"] == 10


@pytest.mark.django_db
@patch("django.db.models.fields.files.ImageFieldFile.save", return_value=None)
@patch("django.db.models.fields.files.ImageFieldFile.delete", return_value=None)
def test_product_create_view_seller(mock_save, mock_delete, user):
    mock_save.return_value = None
    image_path = os.path.join(os.path.dirname(__file__), "test_files", "test_image.png")

    image_mock = SimpleUploadedFile(
        name="test_image.jpg",
        content=open(image_path, "rb").read(),
        content_type="image/jpeg",
    )

    user.user_type = "seller"
    user.save()

    api_client = APIClient()
    api_client.force_authenticate(user=user)

    url = reverse("product-create")

    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
        "currency": "USD",
        "image": image_mock,
    }

    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Product"
    assert response.data["price"] == 10


@pytest.mark.django_db
@patch("django.db.models.fields.files.ImageFieldFile.save", return_value=None)
@patch("django.db.models.fields.files.ImageFieldFile.delete", return_value=None)
def test_product_create_fail(mock_save, mock_delete, user):
    mock_save.return_value = None
    image_path = os.path.join(os.path.dirname(__file__), "test_files", "test_image.png")

    image_mock = SimpleUploadedFile(
        name="test_image.jpg",
        content=open(image_path, "rb").read(),
        content_type="image/jpeg",
    )

    user.user_type = "seller"
    user.save()

    api_client = APIClient()
    api_client.force_authenticate(user=user)

    url = reverse("product-create")

    data = {
        "name": "Product",
        "price": -10,
        "count": 10,
        "currency": "USD",
        "image": image_mock,
    }

    # invalid price
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST

    data["price"] = 10
    data["count"] = -10
    # invalid count
    response = api_client.post(url, data, format="multipart")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_product_update_view_not_admin_nor_seller(api_client_auth, product):
    url = reverse("product-update", args=[product.id])
    data = {
        "name": "Product Updated",
        "price": 20,
        "count": 20,
    }

    response = api_client_auth.patch(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_product_update_view_admin(api_admin_auth, product):
    url = reverse("product-update", args=[product.id])
    data = {
        "name": "Product Updated",
        "price": 20,
        "count": 20,
    }

    response = api_admin_auth.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Product Updated"
    assert response.data["price"] == 20


@pytest.mark.django_db
def test_product_update_view_seller_and_owner(user, product):
    user.user_type = "seller"
    user.save()

    api_client = APIClient()
    api_client.force_authenticate(user=user)

    url = reverse("product-update", args=[product.id])
    data = {
        "name": "Product Updated",
        "price": 20,
        "count": 20,
    }

    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Product Updated"
    assert response.data["price"] == 20
    assert response.data["count"] == 20


@pytest.mark.django_db
def test_product_update_view_seller_not_owner(product):
    user2 = User.objects.create_user(
        email="user2@example.com",
        name="User 2",
        password="testpassword123",
        user_type="seller",
    )
    api_client = APIClient()
    api_client.force_authenticate(user=user2)

    url = reverse("product-update", args=[product.id])
    data = {
        "name": "Product Updated",
        "price": 20,
        "count": 20,
    }

    response = api_client.patch(url, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_product_delete_view_not_admin_nor_seller(api_client_auth, product):
    url = reverse("product-delete", args=[product.id])

    response = api_client_auth.delete(url)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_product_delete_view_admin(api_admin_auth, product):
    url = reverse("product-delete", args=[product.id])

    response = api_admin_auth.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_product_delete_view_seller_and_owner(user, product):
    user.user_type = "seller"
    user.save()

    api_client = APIClient()
    api_client.force_authenticate(user=user)

    url = reverse("product-delete", args=[product.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_product_delete_view_seller_not_owner(product):
    user2 = User.objects.create_user(
        email="user2@example.com",
        name="User 2",
        password="testpassword123",
        user_type="seller",
    )
    api_client = APIClient()
    api_client.force_authenticate(user=user2)

    url = reverse("product-delete", args=[product.id])

    response = api_client.delete(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND
