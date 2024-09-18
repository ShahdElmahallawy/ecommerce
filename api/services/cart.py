from api.models.cart_item import CartItem
from api.selectors.cart import get_cart_by_user, get_cart_item, get_cart_item_by_product
from rest_framework.exceptions import ValidationError
from logging import getLogger

logger = getLogger(__name__)


def add_to_cart(user, product, quantity):
    """Add a product to cart"""
    try:
        cart_item = get_cart_item_by_product(user, product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
        cart = get_cart_by_user(user)
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    cart = get_cart_by_user(user)
    return cart


def remove_from_cart(user, item_id):
    """Remove a product from cart"""
    try:
        item = get_cart_item(user, item_id)
        item.delete()
        cart = get_cart_by_user(user)
        return cart
    except CartItem.DoesNotExist:
        logger.error(f"Item {item_id} does not exist in cart for {user.email}")
        raise ValidationError({"detail": "Item does not exist in cart"})


def clear_cart(user):
    """Clear all products from cart"""
    logger.info(f"Clearing cart for {user.email}")
    CartItem.objects.filter(cart__user=user).delete()
    cart = get_cart_by_user(user)
    return cart


def update_cart_item(user, item_id, quantity):
    """Update quantity of a product in cart"""
    try:
        logger.info(f"Updating item {item_id} in cart for {user.email}")
        item = get_cart_item(user, item_id)
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        cart = get_cart_by_user(user)
        return cart
    except CartItem.DoesNotExist:
        logger.error(f"Item {item_id} does not exist in cart for {user.email}")
        raise ValidationError({"detail": "Item does not exist in cart"})
