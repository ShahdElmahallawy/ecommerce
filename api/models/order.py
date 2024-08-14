from django.db import models
from django.contrib.auth.models import User
from api.models.audit import Audit
from api.models.payment import Payment
class Order(Audit):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    payment_method = models.ForeignKey(Payment,on_delete=models.CASCADE,related_name='payment method')
    # models.CharField(max_length=50, choices=PAYMENT_METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)


    def __str__(self):
        return f'Order #{self.id}'

    def calculate_total_price(self):
        total = sum(item.quantity * item.unit_price for item in self.items.all())
        self.total_price = total
        self.save()