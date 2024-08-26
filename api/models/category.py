from django.db import models
from api.models.audit import Audit

class Category(Audit):
    name = models.CharField(max_length=255, unique=True)
    featured_product = models.ForeignKey('api.Product', on_delete=models.CASCADE, related_name='featured_in_categories', null=True, blank=True)

    def __str__(self):
        return self.name
