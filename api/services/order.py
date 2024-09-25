import logging
from api.selectors.order import get_order_by_id_and_user
from api.models.order import Order
from api.models.product import Product
from api.models.payment import Payment
from api.models.cart import Cart
from api.models.order_item import OrderItem
from django.core.exceptions import ValidationError
from django.db.models import F
from api.selectors.payment import get_payment_by_id, get_payment
from api.selectors.cart import get_cart_by_user
from api.selectors.order import get_order_by_id_and_user
from decimal import Decimal
from rest_framework.response import Response
from api.services.discount import apply_discount_to_order
from rest_framework import status
from api.selectors.store import get_stock_in_default_store
from api.models.inventory import Inventory

logger = logging.getLogger(__name__)


def cancel_order(pk, user):
    order = get_order_by_id_and_user(pk, user)
    if order is None:
        return {"error": "Order not found"}, False

    if order.status == "pending":
        order.status = "cancelled"
        order.save()
        logger.info(f"Order with id {pk} for user {user} was cancelled.")
        return {"status": "Order cancelled"}, True

    logger.warning(f"Order with id {pk} for user {user} cannot be cancelled.")
    return {"error": "Order cannot be cancelled"}, False


def mark_order_as_delivered(order_id, user):
    try:
        order = get_order_by_id_and_user(id=order_id, user=user)
    except Order.DoesNotExist:
        logger.error(f"Order with id {order_id} not found for user {user}.")
        return {"error": "Order not found"}, False

    if order.status == "cancelled":
        logger.error(
            f"Order with id {order_id} cannot be marked as delivered because it's cancelled."
        )
        return {"error": "Order  is cancelled"}, False

    order.status = "delivered"
    order.save()

    logger.info(f"Order with id {order_id} marked as delivered for user {user}.")
    return {"status": "Order delivered"}, True


def create_order_from_cart(user, payment_method, discount_code=None):

    try:
        cart = get_cart_by_user(user)
    except Cart.DoesNotExist:
        raise ValueError("No cart found for the user")

    cart_items = cart.items.all()

    if not cart_items.exists():
        raise ValueError("The cart is empty")

    payment_method = get_payment(user=user, payment_id=payment_method)
    if not payment_method:
        raise ValueError("Invalid payment method")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    if discount_code:
        discounted_price, error = apply_discount_to_order(discount_code, total_price)
        if error:
            raise ValueError("no discount found with this code")

        total_price = discounted_price

    order = Order.objects.create(
        user=user,
        payment_method=payment_method,
        total_price=Decimal(total_price),
        status="pending",
    )

    order_items = []
    product_updates = []

    for cart_item in cart_items:
        product = cart_item.product

        try:
            inventory = Inventory.objects.get(product=product)
        except Inventory.DoesNotExist:
            raise ValueError(
                f"No inventory found for product {product.name} in the default store"
            )

        if get_stock_in_default_store(product) < cart_item.quantity:
            raise ValueError(f"Not enough stock for product {product.name}")
        #
        product_updates.append(
            Inventory(id=inventory.id, stock=F("stock") - cart_item.quantity)
        )
        #
        order_item = OrderItem(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            unit_price=product.price,
        )
        order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)

        Inventory.objects.bulk_update(product_updates, ["stock"])

        cart.items.all().delete()

    return order
