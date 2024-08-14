import logging
from api.selector.order import get_order_by_id_and_user

logger = logging.getLogger(__name__)

def cancel_order(pk, user):
    order = get_order_by_id_and_user(pk, user)
    if order is None:
        return {'error': 'Order not found'}, False
    
    if order.status == 'pending':
        order.status = 'cancelled'
        order.save()
        logger.info(f"Order with id {pk} for user {user} was cancelled.")
        return {'status': 'Order cancelled'}, True

    logger.warning(f"Order with id {pk} for user {user} cannot be cancelled.")
    return {'error': 'Order cannot be cancelled'}, False
