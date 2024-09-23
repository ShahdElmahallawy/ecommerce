from api.models import Inventory


def get_inventory_by_id(inventory_id):
    """
    Get an inventory item by its ID.
    """
    try:
        return Inventory.objects.get(id=inventory_id)
    except Inventory.DoesNotExist:
        return None


def get_inventory_by_id_and_seller(inventory_id, seller):
    """
    Get an inventory item by its ID and seller.
    """
    try:
        return Inventory.objects.get(id=inventory_id, store__seller=seller)
    except Inventory.DoesNotExist:
        return None


def get_inventory_by_seller(seller):
    """
    Get all inventory items for a seller.
    """
    return Inventory.objects.filter(store__seller=seller)
