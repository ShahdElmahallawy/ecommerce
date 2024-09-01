import pytest
from api.models import Product, Category
from api.selectors.product import get_product_by_id, list_products


@pytest.fixture
def category():
    return Category.objects.create(name="Category")


@pytest.fixture
def product(user, category):
    return Product.objects.create(
        name="Product", price=10, count=10, created_by=user, category=category
    )


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
