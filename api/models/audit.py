from django.db import models

class Audit(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True

