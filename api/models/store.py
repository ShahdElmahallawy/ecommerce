from django.db import models
from api.models.audit import Audit
from django.contrib.auth import get_user_model

User = get_user_model()


class Store(Audit):
    """
    Represents a store in the e-commerce platform.

    Attributes:
        seller: A reference to the User who owns the store.
        location: The location of the store.
        is_default_shipping: Indicates whether this store is the default shipping location for the seller.
    """

    name = models.CharField(max_length=255)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="stores")
    location = models.CharField(max_length=255)
    is_default_shipping = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """Overrides the save method to set the default store."""
        if self.is_default_shipping:
            Store.objects.filter(seller=self.seller).update(is_default_shipping=False)

        if Store.objects.filter(seller=self.seller).count() == 0:
            self.is_default_shipping = True

        if self.is_default_shipping == False:
            if (
                Store.objects.filter(
                    seller=self.seller, is_default_shipping=True
                ).count()
                == 0
            ):
                self.is_default_shipping = True

        super(Store, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """Overrides the delete method to set the default store."""
        if self.is_default_shipping:
            raise Exception(
                "Cannot delete default store, set another store as default first"
            )
        super(Store, self).delete(*args, **kwargs)

    def __str__(self):
        """Returns a string representation of the store."""
        return f"{self.seller.username} - {self.location}"
