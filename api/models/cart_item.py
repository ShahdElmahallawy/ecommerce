from django.db import models
from api.models.product import Product
from api.models.cart import Cart
from api.models.audit import Audit

class CartItem(Audit):
    """Model of CartItem

    Fields:
    product: ForeignKey to Product model
    quantity: PositiveIntegerField
    cart: ForeignKey to Cart model
    """

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")

    class Meta:
        unique_together = ["product", "cart"]

    def __str__(self):
        return (
            "product: "
            + str(self.product)
            + ", quantity: "
            + str(self.quantity)
            + ", cart: "
            + str(self.cart)
        )
