from django.db import models
from api.models.product import Product
from api.models.store import Store
from api.models.audit import Audit


class Inventory(Audit):
    """
    Inventory model representing the stock of products in a store.

    Attributes:
        store: Reference to the Store model. When the store is deleted, the inventory is also deleted.
        product: Reference to the Product model. When the product is deleted, the inventory is also deleted.
        stock: The quantity of the product available in the store. Defaults to 0.
    """

    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name="inventory")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField(default=0)

    class Meta:
        unique_together = ["store", "product"]

    def __str__(self):
        """Returns a string representation of the inventory."""
        return f"{self.store} - {self.product} - {self.stock}"
