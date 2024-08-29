from django.contrib.auth import get_user_model
import pytest
from api.models.product import Product
from api.selectors.product_selector import get_all_products, get_product_by_id

from api.models.category import Category

User = get_user_model()


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(user, db, category):
    return Product.objects.create(
        name="Test Product",
        price=100.00,
        description="A sample product description",
        count=5,
        created_by=user,
        category=category,
    )


@pytest.mark.django_db
def test_get_product_by_id(product):
    """
    Test fetching a product by its ID.CartItems
    """
    result = get_product_by_id(product.id)
    assert result == product
    assert result.name == "Test Product"


@pytest.mark.django_db
def test_get_product_by_id_not_found():
    """
    Test that None is returned if no product matches the ID.
    """
    result = get_product_by_id(999)
    assert result is None


@pytest.mark.django_db
def test_get_all_products(product):
    """
    Test getting all products.
    """
    result = list(get_all_products())
    assert len(result) == 1
    assert product in result
