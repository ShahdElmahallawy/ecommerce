from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True)
    featred_product = models.ForeignKey("Product", on_delete=models.CASCADE, related_name='category')

    def __str__(self):
        return self.name