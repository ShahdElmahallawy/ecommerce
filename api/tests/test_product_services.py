import pytest

from api.models import Product

from api.services.product import create_product, update_product, delete_product


@pytest.fixture
def product():
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_create_product():
    product = create_product(
        {
            "name": "Product",
            "price": 10,
            "count": 10,
        }
    )

    assert product.name == "Product"
    assert product.price == 10
    assert product.count == 10


@pytest.mark.django_db
def test_update_product(product):
    updated_product = update_product({"name": "Updated Product"}, product)

    assert updated_product.name == "Updated Product"


@pytest.mark.django_db
def test_delete_product(product):
    delete_product(product)

    assert Product.objects.exclude(is_deleted=True).count() == 0
