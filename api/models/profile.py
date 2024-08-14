from django.db import models
from . import User, Audit


class Profile(Audit):
    """Profile model for users

    Fields:
        user: User associated with the profile
        user_type: Type of the user (seller or customer)
        address: Address of the user
        phone: Phone number of the user
        preferred_currency: Preferred currency of the user
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    USER_TYPES = (
        ("seller", "Seller"),
        ("customer", "Customer"),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="customer")
    address = models.CharField(max_length=255, null=True)
    phone = models.CharField(max_length=11, null=True)
    CURRENCY_CHOICES = (
        ("EGP", "Egyptian Pound"),
        ("MXN", "Mexican Peso"),
        ("SAR", "Saudi Riyal"),
        ("USD", "United States Dollar"),
        ("EUR", "Euro"),
        ("JPY", "Japanese Yen"),
        ("GBP", "British Pound Sterling"),
        ("CHF", "Swiss Franc"),
        ("CAD", "Canadian Dollar"),
        ("AUD", "Australian Dollar"),
        ("INR", "Indian Rupee"),
        ("RUB", "Russian Ruble"),
        ("ZAR", "South African Rand"),
        ("TRY", "Turkish Lira"),
    )
    preferred_currency = models.CharField(
        max_length=3, choices=CURRENCY_CHOICES, null=True
    )

    def __str__(self):
        """Return string representation of the profile"""
        return self.user.email
