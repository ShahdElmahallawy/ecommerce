from django.db import models
from . import User


class Wishlist(models.Model):
    """Model representing a wishlist belonging to a user

    Fields:
        user: The owner of the wishlist
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        """Return string representation of the wishlist"""
        return self.user.email
