from django.db import models
from api.models.user import User
from api.models.audit import Audit
from api.models.payment import Payment
from decimal import Decimal


class Order(Audit):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("delivered", "Delivered"),
        ("cancelled", "Cancelled"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    payment_method = models.ForeignKey(
        Payment, on_delete=models.CASCADE, related_name="payment_method"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    settled = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id}"

    def calculate_total_price(self):
        total = Decimal("0.00")
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_price = total
        self.save()
