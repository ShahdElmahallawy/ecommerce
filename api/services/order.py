from api.models.inventory import Inventory
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
from api.selectors.store import get_stock_in_default_store

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


import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY
from api.selectors.cart import get_cart_items


def create_order_session(request, user, payment_method, discount_code=None):
    items = get_cart_items(user)
    if not items.exists():
        raise ValueError("The cart is empty")

    items_list = []
    for item in items:
        product = item.product

        if product.count < item.quantity:
            raise ValueError(f"Not enough stock for product {product.name}")

        items_list.append(
            {
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": product.name,
                    },
                    "unit_amount": int(item.product.price * 100),
                },
                "quantity": item.quantity,
            }
        )

    cart_id = items.first().cart.id

    session = stripe.checkout.Session.create(
        success_url=f"{request.scheme}://{request.get_host()}/api/orders/redirect?status=success",
        cancel_url=f"{request.scheme}://{request.get_host()}/api/orders/redirect?status=cancel",
        customer_email=request.user.email,
        client_reference_id=cart_id,
        line_items=items_list,
        shipping_options=[
            {
                "shipping_rate_data": {
                    "type": "fixed_amount",
                    "fixed_amount": {
                        "amount": 1000,
                        "currency": "usd",
                    },
                    "display_name": "Shipping takes 5-7 days",
                },
            },
        ],
        mode="payment",
        metadata={"payment_method": payment_method},
    )

    return session


def create_order_from_cart_multiple_stores(user, payment_method, discount_code=None):
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
    inventory_updates = []

    for cart_item in cart_items:
        product = cart_item.product

        if get_stock_in_default_store(product) < cart_item.quantity:
            raise ValueError(f"Not enough stock for product {product.name}")

        inventory_updates.append(
            Inventory(
                product=product,
                store=product.store,
                stock=F("stock") - cart_item.quantity,
            )
        )

        order_item = OrderItem(
            order=order,
            product=product,
            quantity=cart_item.quantity,
            unit_price=product.price,
        )
        order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)

        Inventory.objects.bulk_update(inventory_updates, ["stock"])

        cart.items.all().delete()

    return order
