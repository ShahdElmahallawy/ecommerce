from api.models.store import Store


def get_store_by_id(store_id):
    """
    Get a store by its ID.
    """
    try:
        return Store.objects.exclude(is_deleted=True).get(id=store_id)
    except Store.DoesNotExist:
        return None


def get_store_by_seller(seller, store_id):
    """
    Get a store by its ID and seller.
    """
    try:
        return Store.objects.exclude(is_deleted=True).get(seller=seller, id=store_id)
    except Store.DoesNotExist:
        return None


def get_stores_by_seller(seller):
    """
    Get all stores owned by a seller.
    """
    return Store.objects.exclude(is_deleted=True).filter(seller=seller)


def get_stores():
    """
    Get all stores.
    """
    return Store.objects.exclude(is_deleted=True)


def get_default_shipping_store(seller):
    """
    Get the default shipping store for a seller.
    """
    try:
        return Store.objects.exclude(is_deleted=True).get(
            seller=seller, is_default_shipping=True
        )
    except Store.DoesNotExist:
        return None
