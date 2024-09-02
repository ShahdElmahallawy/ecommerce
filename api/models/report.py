from django.db import models
from api.models.product import Product
from api.models.order import Order
from api.models.user import User
from api.models.audit import Audit


class Report(Audit):
    REPORT_TYPE_CHOICES = (
        ("product", "Product"),
        ("order", "Order"),
    )

    report_type = models.CharField(max_length=7, choices=REPORT_TYPE_CHOICES)
    rid = models.PositiveIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reports")
    message = models.TextField()

    def get_related_object(self):
        if self.report_type == "product":
            return Product.objects.get(id=self.rid)
        elif self.report_type == "order":
            return Order.objects.get(id=self.rid)
