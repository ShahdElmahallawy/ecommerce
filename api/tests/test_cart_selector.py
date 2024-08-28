import pytest
from api.models.cart import Cart
from api.models.cart_items import CartItems
from api.models.product import Product
from api.selectors.cart_selector import get_cart_by_user
from django.contrib.auth.models import User

@pytest.fixture
def user(db):
    return User.objects.create(username='testuser')

@pytest.fixture
def product(db):
    return Product.objects.create(name="Sample Product", price=20.00)

@pytest.fixture
def cart(user, db):
    return Cart.objects.create(user=user)

@pytest.fixture
def cart_item(cart, product, db):
    return CartItems.objects.create(cart=cart, product_id=product, quantity=2)


def test_get_cart_by_user(user, cart):
    fetched_cart = get_cart_by_user(user)
    assert fetched_cart == cart
