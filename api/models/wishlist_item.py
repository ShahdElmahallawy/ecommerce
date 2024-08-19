from django.db import models

from .models import Wishlist
from . import Audit


class WishlistItem(Audit):
    """Model representing an item in a wishlist

    Fields:
        wishlist: The wishlist to which this item belongs
        product: The product that is added to the wishlist
    """

    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="items"
    )
    product = models.ForeignKey("Product", on_delete=models.CASCADE)

    class Meta:
        unique_together = ["wishlist", "product"]

    def __str__(self):
        """Return string representation of the wishlist item"""
        return f"{self.wishlist} - {self.product.name}"
