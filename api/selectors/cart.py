from api.models.cart import Cart
from api.models.cart_item import CartItem


def get_cart_by_user(user):
    cart = Cart.objects.filter(user=user).prefetch_related("items__product").first()
    if not cart:
        cart = Cart.objects.create(user=user)
    return cart


def get_cart_item(user, id):
    """Get a cart item"""
    return CartItem.objects.get(cart__user=user, id=id)


def get_cart_item_by_product(user, product):
    """Get a cart item by product"""
    return CartItem.objects.get(cart__user=user, product=product)
