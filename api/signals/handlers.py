from django.db.models.signals import post_save
from django.dispatch import receiver

from api.models import User, Profile


@receiver(post_save, sender=User)
def create_profile_for_created_user(sender, **kwargs):
    if kwargs["created"]:
        Profile.objects.create(user=kwargs["instance"])
