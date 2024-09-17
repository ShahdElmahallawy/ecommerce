import pytest
from api.models import Product, Category
from api.selectors.product import get_product_by_id, list_products


@pytest.fixture
def user_data():
    return {
        "email": "user@example.com",
        "name": "User Test",
    }


@pytest.fixture
def product(user):
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_get_product_by_id(product):
    assert get_product_by_id(product.id) == product


@pytest.mark.django_db
def test_get_product_by_id_not_found():
    assert get_product_by_id(1) is None


@pytest.mark.django_db
def test_list_products(product):
    products = list_products()

    assert products.count() == 1
    assert products[0] == product
