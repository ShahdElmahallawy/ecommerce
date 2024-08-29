import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category
from django.core.files.uploadedfile import SimpleUploadedFile

@pytest.fixture
def authenticated_client():
    user = User.objects.create_superuser(username='test', password='test')
    client = APIClient()
    client.force_authenticate(user=user)
    return client

@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(category, db, authenticated_client):
    user = authenticated_client.handler._force_user
    product = Product.objects.create(
        name='product1', 
        price=10.00, 
        description='A product1', 
        count=5, 
        category=category, 
        currency='EGP',
        created_by= user,
    )
    print(f"Created Product ID: {product.pk}")  
    return product

@pytest.mark.django_db
def test_retrieve_product(authenticated_client, product):
    url = reverse('products:product-detail', kwargs={'pk': product.pk})
    response = authenticated_client.get(url)
    assert response.status_code == 200
    assert response.data['name'] == 'product1'

@pytest.mark.django_db
def test_create_product(authenticated_client, category):
    url = reverse('products:create-product')
    image_path = '/home/shahd/ecommerce/api/tests/image.png'
    image = SimpleUploadedFile(name='test_image.png', content=open(image_path, 'rb').read(), content_type='image/png')
    data = {
        'name': 'New Product',
        'price': 50.00,
        'description': 'A new product description',
        'count': 15,
        'category': category.id,
        'currency': 'USD',
        'image': image,
        # 'created_by': authenticated_client,
    }
    response = authenticated_client.post(url, data, format='multipart')
    assert response.status_code == 201, f"Expected 201 Created, got {response.status_code}. Details: {response.data}"

@pytest.mark.django_db
def test_update_product(authenticated_client, product):
    url = reverse('products:update-product', kwargs={'pk': product.pk})
    data = {'name': 'Updated Product'}
    response = authenticated_client.put(url, data, format='json')
    assert response.status_code == 200
    product.refresh_from_db()
    assert product.name == 'Updated Product'

@pytest.mark.django_db
def test_delete_product(authenticated_client, product):
    url = reverse('products:delete-product', kwargs={'pk': product.pk})
    print(f"Delete URL: {url}") 
    response = authenticated_client.delete(url)
    print(f"Delete Response: {response.status_code}")  
    assert response.status_code == 204
    assert Product.objects.count() == 0
