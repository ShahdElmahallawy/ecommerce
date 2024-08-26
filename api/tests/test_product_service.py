import pytest
from django.contrib.auth.models import User
from api.models.product import Product
from api.models.category import Category


@pytest.fixture
def user(db):
    return User.objects.create_user(username='testuser', password='password')

@pytest.fixture
def another_user(db):
    return User.objects.create_user(username='anotheruser', password='password')

@pytest.fixture
def category(db):
    return Category.objects.create(name='Test Category')

@pytest.fixture
def product(user, db, category):
    return Product.objects.create(
        name="Test Product",
        price=100.00,
        description="A product",
        count=5, 
        created_by=user,
        category=category,
    )


@pytest.fixture
def update_data():
    return {'name': 'Updated Name', 'price': 150.00}

def test_list_products(product, db):
    from api.service.product_service import list_products
    products = list_products()
    assert len(products) == 1
    assert products[0] == product
def test_retrieve_product(product, db):
    from api.service.product_service import retrieve_product
    fetched_product = retrieve_product(product.id)
    assert fetched_product == product

def test_retrieve_product_not_found(db):
    from api.service.product_service import retrieve_product
    fetched_product = retrieve_product(999)
    assert fetched_product is None
def test_update_product(product, user, update_data, db):
    from api.service.product_service import update_product
    updated_product = update_product(product.id, user, update_data)
    assert updated_product.name == update_data['name']

def test_update_product_unauthorized(product, another_user, update_data, db):
    from api.service.product_service import update_product
    updated_product = update_product(product.id, another_user, update_data)
    assert updated_product is None

def delete_product(product_id, user):
    product = Product.objects.filter(pk=product_id, created_by=user).first()
    if product and not product.is_deleted:
        product.is_deleted = True
        product.save()
        return True
    return False


