import hashlib
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from api.models import Profile


def get_user_profile(user):
    return get_object_or_404(Profile, user=user)
