from api.models.audit import Audit
from api.models.user import User
from django_countries.fields import CountryField
from django.db import models


class Address(Audit):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_address = models.CharField(max_length=100)
    apartment_address = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    zip = models.IntegerField()
    address_type = models.CharField(max_length=10)
    default = models.BooleanField(default=False)

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        user_addresses = self.__class__.objects.filter(user=self.user)
        if not user_addresses.exists():
            self.default = True
        elif self.default:
            user_addresses.update(default=False)
        else:
            self.default = False

        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.user.username
