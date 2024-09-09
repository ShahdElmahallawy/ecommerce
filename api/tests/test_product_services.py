import pytest

from api.models import Product, Category

from api.services.product import create_product, update_product, delete_product


@pytest.fixture
def category():
    return Category.objects.create(name="Category")


@pytest.fixture
def product(user, category):
    return Product.objects.create(
        name="Product", price=10, count=10, created_by=user, category=category
    )


@pytest.mark.django_db
def test_create_product(user, category):
    product = create_product(
        {
            "name": "Product",
            "price": 10,
            "count": 10,
            "created_by": user,
            "category": category,
        }
    )

    assert product.name == "Product"
    assert product.price == 10
    assert product.count == 10
    assert product.created_by == user
    assert product.category == category


@pytest.mark.django_db
def test_update_product(product):
    updated_product = update_product({"name": "Updated Product"}, product)

    assert updated_product.name == "Updated Product"


@pytest.mark.django_db
def test_delete_product(product):
    delete_product(product)

    assert Product.objects.count() == 0
