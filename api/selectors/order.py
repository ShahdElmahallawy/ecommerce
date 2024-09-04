import logging
from api.models.order import Order

logger = logging.getLogger(__name__)


def get_order_by_id_and_user(pk, user):
    try:
        order = Order.objects.select_related("user").get(pk=pk, user=user)
        return order
    except Order.DoesNotExist:
        logger.error(f"Order with id {pk} for user {user} not found.")
        return None


def get_orders_by_user(user):
    return Order.objects.filter(user=user)

def get_order_by_id(order_id):

    try:
        order = Order.objects.prefetch_related('items__product').get(id=order_id)
    except Order.DoesNotExist:
        return None

    return order