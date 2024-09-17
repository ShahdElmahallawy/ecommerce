import pytest
from api.selectors.cart import get_cart_by_user, get_cart_item
from .factories import UserFactory, ProductFactory, CartFactory, CartItemFactory


@pytest.fixture
def user(db):
    """Fixture to create a user."""
    return UserFactory()


@pytest.fixture
def product(db):
    """Fixture to create a product."""
    return ProductFactory(image=None)


@pytest.mark.django_db
def test_get_cart_by_user(user):
    """Test for fetching the cart by user."""
    cart = get_cart_by_user(user)
    assert cart is not None
    assert cart.user == user


@pytest.mark.django_db
def test_get_cart_item(user, product):
    """Test for fetching a cart item by user."""
    cart = get_cart_by_user(user)

    cart_item = CartItemFactory(product=product, cart=cart)

    item = get_cart_item(user, cart_item.id)
    assert item is not None
    assert item == cart_item
    assert item.product == product
    assert item.cart == cart
