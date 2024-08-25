import hashlib
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.contrib.auth import get_user_model


def get_user_by_email(email):
    User = get_user_model()
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return None
    return user


def get_user_by_reset_token(token):
    User = get_user_model()
    hashed_token = hashlib.sha256(token.encode()).hexdigest()
    return User.objects.filter(
        reset_password_token=hashed_token,
        reset_password_token_expiry__gt=timezone.now(),
    ).first()
