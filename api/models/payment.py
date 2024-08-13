from django.db import models
from . import User


class Payment(models.Model):
    """
    Model representing a payment.

    Fields:
        user: The user who made the payment.
        pan: The PAN of the payment.
        bank_name: The name of the bank associated with the payment.
        expiry_date: The expiry date of the payment.
        cvv: The CVV of the payment.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pan = models.CharField(max_length=16, unique=True)
    bank_name = models.CharField(max_length=255)
    expiry_date = models.DateField()
    cvv = models.CharField(max_length=3)

    def __str__(self):
        """Returns a string representation of the payment."""
        return f"{self.user.username} - bank: {self.bank_name}"
