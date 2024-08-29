from api.models.cart import Cart
from api.models.cart_items import CartItems
import logging

logger = logging.getLogger(__name__)


def get_cart_by_user(user):
    """
    Retrieve a user's cart.
    """
    return Cart.objects.get(user=user)


def get_cart_items(cart):
    """
    Retrieve all items in a user's cart.
    """
    return cart.cartitems_set.all()


def get_cart_item(cart, product_id):
    """
    Retrieve a specific cart item by product ID within the given cart.
    """
    try:
        return CartItems.objects.get(cart=cart, product_id=product_id)
    except CartItems.DoesNotExist:
        logger.warning(
            f"Cart item with product ID {product_id} not found in cart {cart.id}"
        )
        return None
