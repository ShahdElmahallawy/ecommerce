from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from api.models.user import User
from api.models.audit import Audit


class Discount(Audit):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discounts")
    code = models.CharField(max_length=12, unique=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.discount_percentage}% discount for {self.user.email} with code {self.code}"

    def save(self, *args, **kwargs):

        self._validate_is_active()

        super().save(*args, **kwargs)

    def _validate_is_active(self):

        now = timezone.now()
        if now > self.start_date + timedelta(minutes=5):
            self.is_active = False
