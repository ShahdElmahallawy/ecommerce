from django.db import models
from django.utils import timezone


class Product(models.Model):
    """Model of product.

    Fields:
    - name: name of product
    - price: price of product
    - description: description of product
    - image: image of product
    - count: count of product
    - currency: currency of product
    """

    # add viladation to name to be not null
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to="products")
    count = models.PositiveIntegerField()
    currency = models.CharField(max_length=3)

    def __str__(self):
        return self.name
