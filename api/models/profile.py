from django.db import models
from . import User, Audit

from api.constants import CURRENCY_CHOICES

from api.models.address import Address



class Profile(Audit):
    """Profile model for users

    Fields:
        user: User associated with the profile
        user_type: Type of the user (seller or customer)
        address: Address of the user
        phone: Phone number of the user
        preferred_currency: Preferred currency of the user
    """
    USER_TYPES = (
        ("seller", "Seller"),
        ("customer", "Customer"),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="customer")
    address = models.ForeignKey(
        Address, related_name="shipping_address", on_delete=models.SET_NULL, null=True
    )

    phone = models.CharField(max_length=11, null=True)

    preferred_currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, null=True
    )

    def __str__(self):
        """Return string representation of the profile"""
        return self.user.email
