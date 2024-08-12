from django.db import models
from . import User


class Profile(models.Model):
    """Profile model for users

    Fields:
        user: User associated with the profile
        type: Type of the user (seller or customer)
        address: Address of the user
        phone: Phone number of the user
        preferred_currency: Preferred currency of the user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = (
        ("seller", "Seller"),
        ("customer", "Customer"),
    )
    type = models.CharField(max_length=10, choices=USER_TYPES, default="customer")
    address = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    preferred_currency = models.CharField(max_length=3, blank=True, null=True)

    def __str__(self):
        """Return string representation of the profile"""
        return self.user.email
