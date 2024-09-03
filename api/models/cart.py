from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Cart(models.Model):
    """
    Cart model

    Fields:
    user: ForeignKey to User model
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "user: " + str(self.user) + ", items: " + str(self.items)
