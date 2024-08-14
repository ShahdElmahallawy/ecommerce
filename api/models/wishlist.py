from django.db import models
from . import User, Audit


class Wishlist(Audit):
    """Model representing a wishlist belonging to a user

    Fields:
        user: The owner of the wishlist
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the wishlist"""
        return f"{self.user.email}'s wishlist"
