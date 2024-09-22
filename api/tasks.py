import os
from django.core.mail import send_mail
from collections import defaultdict
from api.models import Product
from celery import shared_task
from logging import getLogger
from datetime import timedelta
from django.utils import timezone
from api.models.order import Order
from decimal import Decimal


logger = getLogger(__name__)


@shared_task
def send_restock_mails():
    products = Product.objects.select_related("created_by", "supplier").filter(
        count__lte=5, created_by__isnull=False
    )

    seller_products = defaultdict(list)
    for product in products:
        seller_products[product.created_by].append(product)
    logger.info(seller_products)
    for seller, products in seller_products.items():
        product_list = "\n".join(
            [
                f"{product.name} (Supplier: {product.supplier.name} - contact:{product.supplier.email}) - {product.count} left"
                for product in products
            ]
        )
        email_body = (
            f"The following products are low on stock:\n\n{product_list}\n\n"
            "Please restock them by contacting the respective suppliers.\n\n"
            "Ecommerce Team.\nCEO: Amr"
        )
        try:
            send_mail(
                "Restock products",
                email_body,
                os.getenv("EMAIL_USERNAME"),
                [seller.email],
                fail_silently=False,
            )
        except Exception as e:
            logger.error(
                f"Periodic task failed: failed to send email to {seller.email}, {e}"
            )
        logger.info(f"Email sent to {seller.email}, products: {product_list}")
    logger.info("Periodic task completed, restock emails sent")


@shared_task
def process_settlements():
    logger.info("Starting settlement process for sellers")

    try:
        cutoff_date = timezone.now() - timedelta(days=14)

        orders_to_settle = Order.objects.filter(
            status="delivered", updated_at__lte=cutoff_date, settled=False
        )

        if not orders_to_settle.exists():
            logger.info("No orders found to settle.")
            return "No orders to settle"

        seller_earnings = defaultdict(Decimal)

        for order in orders_to_settle:
            logger.info(
                f"Settling Order #{order.id} for User {order.user.name}, Amount: {order.total_price}"
            )
            for item in order.items.all():
                product = item.product
                seller = product.created_by.name
                earnings = item.quantity * item.unit_price
                seller_earnings[seller] += earnings

            order.settled = True
            order.save()

        for seller, total_earnings in seller_earnings.items():
            logger.info(
                f"Mock sending message to Seller {seller}: 'Your total earnings are ${total_earnings:.2f}'"
            )

        logger.info(f"Successfully settled {orders_to_settle.count()} orders.")
        return f"Settled {orders_to_settle.count()} orders"

    except Exception as e:
        logger.error(f"Error during settlement process: {e}", exc_info=True)
        raise e
