from api.models.order_item import OrderItem


def get_seller_order_items(seller):

    return OrderItem.objects.filter(product__created_by=seller)
