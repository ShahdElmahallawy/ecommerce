from django.core.files.uploadedfile import SimpleUploadedFile
import os
from django.urls import reverse
from rest_framework import status
import pytest
from rest_framework.test import APIClient
from api.models import Product, Category


from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def category():
    return Category.objects.create(name="Category")


@pytest.fixture
def product(user, category):
    return Product.objects.create(
        name="Product", price=10, count=10, created_by=user, category=category
    )


@pytest.fixture
def upload_image():
    image_path = os.path.join(os.path.dirname(__file__), "test_files", "test_image.png")
    with open(image_path, "rb") as image_file:
        image = SimpleUploadedFile(
            name="test_image.jpg", content=image_file.read(), content_type="image/jpeg"
        )
    return image


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
def test_product_create_view_not_admin_nor_seller(api_client_auth, category):
    url = reverse("product-create")
    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
        "category": category,
    }

    response = api_client_auth.post(url, data)

    assert response.status_code == status.HTTP_403_FORBIDDEN


@pytest.mark.django_db
def test_product_create_view_admin(api_admin_auth, category, upload_image):
    url = reverse("product-create")

    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
        "category": category.id,
        "currency": "USD",
        "image": upload_image,
    }

    response = api_admin_auth.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Product"
    assert response.data["price"] == 10


@pytest.mark.django_db
def test_product_create_view_seller(user, category, upload_image):
    user.user_type = "seller"
    user.save()

    api_client = APIClient()
    api_client.force_authenticate(user=user)

    url = reverse("product-create")

    data = {
        "name": "Product",
        "price": 10,
        "count": 10,
        "category": category.id,
        "currency": "USD",
        "image": upload_image,
    }

    response = api_client.post(url, data, format="multipart")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Product"
    assert response.data["price"] == 10


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
