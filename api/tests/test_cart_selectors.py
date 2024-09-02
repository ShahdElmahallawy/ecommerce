import pytest
from api.selectors.cart import get_cart_by_user, get_cart_item
from api.models import Cart, CartItem, Product


@pytest.fixture
def product(db):
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_get_cart_by_user(user):
    cart = get_cart_by_user(user)
    assert cart is not None
    assert cart.user == user


@pytest.mark.django_db
def test_get_cart_item(user, product):
    cart = get_cart_by_user(user)
    cart_item = CartItem.objects.create(cart=cart, product=product, quantity=1)
    item = get_cart_item(user, cart_item.id)
    assert item is not None
    assert item == cart_item
    assert item.product == product
    assert item.quantity == 1
    assert item.cart == cart
