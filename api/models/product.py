
from django.db import models
from django.utils import timezone
from api.models.category import Category
from django.contrib.auth import get_user_model


User = get_user_model()



class Product(models.Model):
    """Model of product.

    Fields:
    - name: name of product
    - price: price of product
    - description: description of product
    - image: image of product
    - count: count of product
    - currency: currency of product
    -feedback: feedback of product
    - rate: rate of product
    - total_rate: total rate of product (average of all rates)
    """

    # category = models.ForeignKey('Category', on_delete=models.CASCADE)
    from api.models.category import Category

    # add viladation to name to be not null
    name = models.CharField(max_length=255, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()


    image = models.ImageField(upload_to="products")
    count = models.PositiveIntegerField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3)
    feedback = models.TextField()
    rate = models.PositiveIntegerField()
    total_rate = models.PositiveIntegerField()

    def __str__(self):

        # from api.models.category import Category
        return self.name


