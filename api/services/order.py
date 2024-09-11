import logging
from api.selectors.order import get_order_by_id_and_user
from api.models.order import Order
from api.models.product import Product
from api.models.payment import Payment
from api.models.cart import Cart
from api.models.order_item import OrderItem
from django.core.exceptions import ValidationError
from django.db.models import F


from decimal import Decimal

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
        order = Order.objects.get(id=order_id, user=user)
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


def create_order_from_cart(user, payment_method):

    try:
        cart = Cart.objects.prefetch_related("items__product").get(user=user)
    except Cart.DoesNotExist:
        raise ValueError("No cart found for the user")

    cart_items = cart.items.all()

    if not cart_items.exists():
        raise ValueError("The cart is empty")

    try:
        payment_method = Payment.objects.get(id=payment_method)
    except Payment.DoesNotExist:
        raise ValueError("Invalid payment method")

    total_price = sum(item.product.price * item.quantity for item in cart_items)

    order = Order.objects.create(
        user=user,
        payment_method=payment_method,
        total_price=Decimal(total_price),
        status="pending",
    )

    order_items = [
        OrderItem(
            order=order,
            product=cart_item.product,
            quantity=cart_item.quantity,
            unit_price=cart_item.product.price,
        )
        for cart_item in cart_items
    ]

    OrderItem.objects.bulk_create(order_items)

    cart.items.all().delete()

    return order
