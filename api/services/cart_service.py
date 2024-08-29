from api.selectors.cart_selector import (
    get_cart_by_user,
    get_cart_item,
    get_cart_items,
)
import logging
from api.models.cart_items import CartItems
from api.models.product import Product
from api.models.cart import Cart

logger = logging.getLogger(__name__)

from django.db.models import ObjectDoesNotExist


def add_product_to_cart(user, product_id, quantity):
    try:
        cart = Cart.objects.get(user=user)
        logger.info(f"Cart found for user {user}")
    except Cart.DoesNotExist:
        logger.info(f"Cart not found for user {user}")
        cart = Cart.objects.create(user=user)  # Create a cart if it does not exist
        logger.info(f"Cart created for user {user}")

    product = Product.objects.get(pk=product_id)
    try:
        cart_item = CartItems.objects.get(cart=cart, product_id=product)
        cart_item.quantity += quantity
        cart_item.save()
        logger.info(
            f"Product {product_id} already exists in cart. Quantity updated to {cart_item.quantity}"
        )
    except CartItems.DoesNotExist:
        CartItems.objects.create(cart=cart, product_id=product, quantity=quantity)
        logger.info(f"Product {product_id} added to cart with quantity {quantity}")

    return cart


def remove_product_from_cart(user, product_id):
    """
    Service to remove a product from the cart.
    """
    cart = get_cart_by_user(user)
    cart_item = get_cart_item(cart, product_id)
    if cart_item:
        cart_item.delete()
        logger.info(f"Product {product_id} removed from cart")


def calculate_cart_total(user):
    """
    Service to calculate the total price of all items in the cart.
    """
    cart = get_cart_by_user(user)
    total = 0
    for item in get_cart_items(cart):
        total += item.quantity * item.product_id.price
        logger.info(
            f"Item: {item.product_id.name}, Quantity: {item.quantity}, Price: {item.product_id.price}"
        )
    return total


def checkout_cart(user):
    """
    Service to handle checkout logic. Placeholder for actual implementation.
    """
    total = calculate_cart_total(user)
    return {"status": "Checkout complete", "total": total}
