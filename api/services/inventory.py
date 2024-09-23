from api.models import Inventory, Product, Store


def create_inventory(seller, data):
    """
    Create an inventory item.
    """
    inventory = Inventory.objects.create(
        store=Store.objects.get(seller=seller, id=data["store"]),
        product=Product.objects.get(id=data["product"]),
        stock=data["stock"],
    )
    inventory.save()
    return inventory


def update_inventory(inventory, data):
    """
    Update an inventory item.
    """
    for key, value in data.items():
        setattr(inventory, key, value)
    inventory.save(update_fields=data.keys())
    return inventory


def delete_inventory(inventory):
    """
    Delete an inventory item.
    """
    inventory.delete()

    return inventory
