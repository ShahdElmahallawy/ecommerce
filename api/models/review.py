from . import Audit
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Review(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(
        "Product", on_delete=models.CASCADE, related_name="reviews"
    )
    text = models.TextField()
    rating = models.FloatField()

    class Meta:
        unique_together = ("user", "product")

    def __str__(self):
        return f"{self.user} - {self.product} - review"
