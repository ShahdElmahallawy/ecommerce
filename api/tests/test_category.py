import pytest
from django.urls import reverse
from rest_framework import status
from api.models import Category


@pytest.mark.django_db
def test_create_category_success(api_admin_auth, product):
    url = reverse("categories:create-category")
    data = {"name": "Electronics", "featured_product": product.id}

    response = api_admin_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["name"] == "Electronics"
    assert response.data["featured_product"] == product.id

    category = Category.objects.get(name="Electronics")
    assert category is not None
    assert category.featured_product == product


@pytest.mark.django_db
def test_create_category_missing_name(api_admin_auth, product):

    url = reverse("categories:create-category")
    data = {"featured_product": product.id}

    response = api_admin_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "name" in response.data


@pytest.mark.django_db
def test_create_category_invalid_featured_product(api_admin_auth):
    url = reverse("categories:create-category")
    data = {"name": "Invalid Product Category", "featured_product": 9999}

    response = api_admin_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "featured_product" in response.data
