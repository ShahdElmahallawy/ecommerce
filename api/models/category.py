from django.db import models
from api.models.product import Product
from api.models.audit import Audit


class Category(Audit):
    name = models.CharField(max_length=255, unique=True)
    featured_product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='featured_product', null=True, blank=True)

    def __str__(self):
        return self.name
