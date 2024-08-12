from django.db import models
from django.utils import timezone
# from api.models.user import User
from django.contrib.auth import get_user_model

User = get_user_model()

class Cart(models.Model):
    """Model of cart.

    Fields:
    - user: user of cart (one to one relation)
    - items: items of cart (one to many relation), one cart can have many items
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.JSONField(default=list)

    def __str__(self):
        return str(self.items)