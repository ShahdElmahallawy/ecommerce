from django.db import models
from django.contrib.auth import get_user_model
from api.models.audit import Audit

User = get_user_model()


class Cart(Audit):
    """
    Cart model

    Fields:
    user: ForeignKey to User model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "user: " + str(self.user) + ", items: " + str(self.items)
