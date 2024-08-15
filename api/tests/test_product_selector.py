import pytest
from api.models.product import Product
from api.selector.product_selector import get_all_products, get_all_products_with_details, get_product_by_id, get_products_by_category

@pytest.fixture
def product(db):
    return Product.objects.create(name="Test Product", price=100.00, description="A sample product description")


def test_get_product_by_id(product):
    """
    Test fetching a product by its ID.
    """
    result = get_product_by_id(product.id)
    assert result == product
    assert result.name == "Test Product"

def test_get_product_by_id_not_found():
    """
    Test that None is returned if no product matches the ID.
    """
    result = get_product_by_id(999) 
    assert result is None

def test_get_all_products(product):
    """
    Test getting all products.
    """
    result = list(get_all_products())
    assert len(result) == 1
    assert product in result
