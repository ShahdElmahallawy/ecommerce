import os
from django.core.mail import send_mail
from collections import defaultdict
from api.models import Product
from celery import shared_task
from logging import getLogger

logger = getLogger(__name__)


@shared_task
def send_restock_mails():
    products = Product.objects.filter(count__lte=5, created_by__isnull=False)

    seller_products = defaultdict(list)
    for product in products:
        seller_products[product.created_by].append(product)
    logger.info(seller_products)
    for seller, products in seller_products.items():
        product_list = "\n".join(
            [f"{product.name} ({product.count} left)" for product in products]
        )
        email_body = f"The following products are low on stock:\n\n{product_list}\n\nPlease restock them.\n\n Ecommerce Team.\n CEO: Amr"
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
