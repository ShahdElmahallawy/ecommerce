from django.db import models
from . import Audit


class Supplier(Audit):
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return self.name
