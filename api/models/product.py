from django.db import models
from django.utils import timezone
from api.models.category import Category
from django.contrib.auth import get_user_model

User = get_user_model()


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
    - category: category of product
    - currency: currency of product
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
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='products')


    def __str__(self):
        # from api.models.category import Category
        return self.name

