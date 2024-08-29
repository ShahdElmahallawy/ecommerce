from django.db import models

from api.models.user import User
from api.models.audit import Audit


class Payment(Audit):
    """
    Model representing a payment.

    Fields:
        user: The user who made the payment.
        pan: The PAN of the payment.
        bank_name: The name of the bank associated with the payment.
        expiry_date: The expiry date of the payment.
        cvv: The CVV of the payment.
        card_type: Type of the card (credit or debit)
    """

    CARD_TYPES = (
        ("credit", "Credit"),
        ("debit", "Debit"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pan = models.CharField(max_length=16, unique=True)
    bank_name = models.CharField(max_length=255)
    expiry_date = models.DateField(null=True)
    cvv = models.CharField(max_length=3)
    card_type = models.CharField(max_length=10, choices=CARD_TYPES)
    default = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overrides the save method to set the default payment."""

        if self.default:
            Payment.objects.filter(user=self.user).update(default=False)

        if Payment.objects.filter(user=self.user).count() <= 1:
            self.default = True

        super(Payment, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Overrides the delete method to set the default payment."""
        if self.default:
            raise Exception(
                "Cannot delete default payment, set another payment as default first"
            )
        super(Payment, self).delete(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the payment."""
        return f"{self.user.username} - bank: {self.bank_name}"
