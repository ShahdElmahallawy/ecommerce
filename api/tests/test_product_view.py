import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category


@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def create_user(db):
    return User.objects.create_user(username='shahd', password='shahd123')

@pytest.fixture
def create_category(db):
    return Category.objects.create(name='Home')

@pytest.fixture
def create_product(db, create_user, create_category):
    return Product.objects.create(
        name="product1",
        price=100.00,
        description="description1",
        count=10,
        category=create_category,
        currency='EGP',
        image=None
    )

@pytest.fixture
def auth_client(api_client, create_user):
    api_client.force_authenticate(user=create_user)
    return api_client

def test_list_products(authenticated_client, product):
    url = reverse('product-list')
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['name'] == 'product1'

# def test_retrieve_product(auth_client, create_product):
#     url = reverse('product-detail', kwargs={'pk': create_product.pk})
#     response = auth_client.get(url)
#     assert response.status_code == 200
#     assert response.data['name'] == 'product1'

# def test_create_product(auth_client):
#     url = reverse('product-list')
#     data = {
#         'name': 'New Product',
#         'price': 50.00,
#         'description': 'A new test product',
#         'count': 15,
#         'category': create_category.pk,
#         'currency': 'USD'
#     }
#     response = auth_client.post(url, data, format='json')
#     assert response.status_code == 201
#     assert Product.objects.count() == 1

# def test_update_product(auth_client, create_product):
#     url = reverse('product-detail', kwargs={'pk': create_product.pk})
#     data = {'name': 'Updated Product'}
#     response = auth_client.patch(url, data, format='json')
#     assert response.status_code == 200
#     create_product.refresh_from_db()
#     assert create_product.name == 'Updated Product'

# def test_delete_product(auth_client, create_product):
#     url = reverse('product-detail', kwargs={'pk': create_product.pk})
#     response = auth_client.delete(url)
#     assert response.status_code == 204
#     assert Product.objects.count() == 0
