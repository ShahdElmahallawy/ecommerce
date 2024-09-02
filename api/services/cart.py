from api.models import CartItem
from api.selectors.cart import get_cart_by_user, get_cart_item
from rest_framework.exceptions import ValidationError


def add_to_cart(user, product, quantity):
    """Add a product to cart"""
    cart = get_cart_by_user(user)
    try:
        cart_item = CartItem.objects.get(cart=cart, product=product)
        cart_item.quantity += quantity
        cart_item.save()
    except CartItem.DoesNotExist:
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
        raise ValidationError({"detail": "Item does not exist in cart"})


def clear_cart(user):
    """Clear all products from cart"""
    CartItem.objects.filter(cart__user=user).delete()
    cart = get_cart_by_user(user)
    return cart


def update_cart_item(user, item_id, quantity):
    """Update quantity of a product in cart"""
    try:
        item = get_cart_item(user, item_id)
        item.quantity = quantity
        item.save(update_fields=["quantity"])
        cart = get_cart_by_user(user)
        return cart
    except CartItem.DoesNotExist:
        raise ValidationError({"detail": "Item does not exist in cart"})
