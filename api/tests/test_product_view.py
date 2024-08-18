import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category

@pytest.fixture
def authenticated_client():
    user = User.objects.create_user(username='test', password='test')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def create_category():
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(create_category):
    return Product.objects.create(name='product1', price=10.00, description='A product1', count=5, category=create_category, currency='EGP')

def test_retrieve_product(authenticated_client, product):
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'product1'

def test_create_product(authenticated_client, create_category):
    url = reverse('product-list')
    data = {
        'name': 'New Product',
        'price': 50.00,
        'description': 'A new product1',
        'count': 15,
        'category': create_category.pk,
        'currency': 'EGP'
    }
    response = authenticated_client.post(url, data, format='json')
    assert response.status_code == 201
    assert Product.objects.count() == 1

def test_update_product(authenticated_client, product):
    url = reverse('product-detail', kwargs={'pk': product.pk})
    data = {'name': 'Updated Product'}
    response = authenticated_client.patch(url, data, format='json')
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == 'Updated Product'

def test_delete_product(authenticated_client, product):
    url = reverse('product-detail', kwargs={'pk': product.pk})
    response = authenticated_client.delete(url)
    assert response.status_code == 204
    assert Product.objects.count() == 0
