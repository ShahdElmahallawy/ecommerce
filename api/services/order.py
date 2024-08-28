import logging
from api.selectors.order import get_order_by_id_and_user
from api.models.order import Order
from api.models.product import Product
from api.models.order_item import OrderItem
from django.core.exceptions import ValidationError

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


def create_order(user, payment_method, items):
    order = Order.objects.create(user=user, payment_method=payment_method)
    total_price = Decimal("0.00")

    for item_data in items:
        product = Product.objects.get(id=item_data["product_id"])
        quantity = item_data["quantity"]

        if product.count < quantity:
            raise ValidationError(f"Insufficient stock for product {product.name}")

        product.count -= quantity
        product.save()

        unit_price = Decimal(product.price)
        total_price += quantity * unit_price

        OrderItem.objects.create(
            order=order, product=product, quantity=quantity, unit_price=unit_price
        )

    order.total_price = total_price
    order.save()

    return order


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
