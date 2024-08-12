from django.db import models
from django.utils import timezone
# from api.models.user import User
from api.models.product import Product
from api.models.cart import Cart
from django.contrib.auth import get_user_model

User = get_user_model()
class CartItems(models.Model):
    """Model of cart.

    Fields:
    -product_id: product id of product in cart
    -quantity: quantity of product in cart
    -cart: cart of cart items 
    """
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)

    def __str__(self):
        return "product_id: "+str(self.product_id) + ", quantity: " + str(self.quantity)