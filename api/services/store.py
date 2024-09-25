from api.models.store import Store


def create_store(seller, data):
    """
    Create a new store.
    """
    store = Store(seller=seller, **data)
    store.save()
    return store


def update_store(store, data):
    """
    Update a store.
    """
    for key, value in data.items():
        setattr(store, key, value)
    store.save(update_fields=data.keys())
    return store


def delete_store(store):
    """
    Delete a store.
    """
    store.is_deleted = True
    store.save(update_fields=["is_deleted"])
    return store
