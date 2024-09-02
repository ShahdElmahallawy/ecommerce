from api.models import Cart, CartItem


def get_cart_by_user(user):
    cart, created = Cart.objects.get_or_create(user=user)
    if not created:
        cart = Cart.objects.prefetch_related("items__product").get(user=user)
    return cart


def get_cart_item(user, id):
    """Get a cart item"""
    return CartItem.objects.get(cart__user=user, id=id)
