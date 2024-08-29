import pytest
from api.models.cart import Cart
from api.models.cart_items import CartItems
from api.models.product import Product
from api.models.category import Category
from api.selectors.cart_selector import get_cart_by_user
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def category(db):
    return Category.objects.create(name="Test Category")


@pytest.fixture
def product(db, category):
    return Product.objects.create(
        name="Sample Product", price=20.00, count=10, category=category
    )


@pytest.fixture
def cart(user, db):
    return Cart.objects.create(user=user)


@pytest.fixture
def cart_item(cart, product, db):
    return CartItems.objects.create(cart=cart, product_id=product, quantity=2)


def test_get_cart_by_user(user, cart):
    fetched_cart = get_cart_by_user(user)
    assert fetched_cart == cart
