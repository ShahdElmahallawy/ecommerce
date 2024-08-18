import os
import hashlib
from datetime import timedelta

from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from api.utils import send_password_reset_email


def create_user(validated_data):
    """
    Service creates a new user.

    Returns:
        tokens: The refresh and access tokens.
    """
    User = get_user_model()
    user = User.objects.create_user(**validated_data)
    refresh = RefreshToken.for_user(user)
    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return tokens


def generate_reset_password_token(user, request):
    reset_token = os.urandom(32).hex()
    user.reset_password_token = hashlib.sha256(reset_token.encode()).hexdigest()
    user.reset_password_token_expiry = timezone.now() + timedelta(minutes=15)
    user.save(update_fields=["reset_password_token", "reset_password_token_expiry"])

    reset_link = request.build_absolute_uri(
        reverse("reset-password", kwargs={"token": reset_token})
    )
    send_password_reset_email(user, reset_link)


def reset_user_password(user, new_password):
    user.set_password(new_password)
    user.reset_password_token = None
    user.reset_password_token_expiry = None
    user.save(
        update_fields=[
            "password",
            "reset_password_token",
            "reset_password_token_expiry",
        ]
    )
