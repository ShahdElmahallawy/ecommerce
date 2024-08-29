from django.db import models
from django.contrib.auth import get_user_model
from api.models.audit import Audit

User = get_user_model()


class Cart(Audit):
    """Model of cart.

    Fields:
    - user: user of cart (one to one relation)
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "user: " + str(self.user) + ", items: " + str(self.items)
