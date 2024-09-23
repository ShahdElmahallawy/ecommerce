from django.db import models
from api.models.audit import Audit
from django.contrib.auth import get_user_model

User = get_user_model()


class Store(Audit):
    """
    Represents a store in the e-commerce platform.

    Attributes:
        seller: A reference to the User who owns the store.
        location: The location of the store.
        is_default_shipping: Indicates whether this store is the default shipping location for the seller.
    """

    name = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
    location = models.CharField(max_length=255)
    is_default_shipping = models.BooleanField(default=False)

    def __str__(self):
        """Returns a string representation of the store."""
        return f"{self.seller.username} - {self.location}"
