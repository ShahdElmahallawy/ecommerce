import os
import hashlib
from datetime import timedelta
from rest_framework.exceptions import ValidationError
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.exceptions import APIException
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


def get_tokens_for_user(validated_data):
    """
    Service to get tokens for user.

    Returns:
        tokens: The refresh and access tokens.
    """
    refresh = RefreshToken.for_user(validated_data)
    tokens = {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }
    return tokens


def get_refreshed_tokens(validated_data):
    """
    Validate the refresh token and return a new access token.

    Returns:
        dict: A dictionary containing the new access token.
    """
    try:
        refresh = RefreshToken(validated_data)
        new_access_token = str(refresh.access_token)
    except TokenError as e:
        raise ValidationError({"refresh": str(e)})

    return {"access": new_access_token, "refresh": validated_data}


def generate_reset_password_token(user, request):
    """
    Generates a reset password token and sends the reset email.
    """
    reset_token = os.urandom(32).hex()
    user.reset_password_token = hashlib.sha256(reset_token.encode()).hexdigest()
    user.reset_password_token_expiry = timezone.now() + timedelta(minutes=15)
    user.save(update_fields=["reset_password_token", "reset_password_token_expiry"])

    reset_link = request.build_absolute_uri(
        reverse("password-reset", args=[reset_token])
    )
    try:
        send_password_reset_email(user, reset_link)
    except Exception:
        raise APIException(
            "Failed to send password reset email. Please try again later."
        )


def reset_user_password(user, new_password):
    user.set_password(new_password)
    user.reset_password_token = None
    user.reset_password_token_expiry = None
    user.password_changed_at = timezone.now()
    user.save(
        update_fields=[
            "password",
            "reset_password_token",
            "reset_password_token_expiry",
            "password_changed_at",
        ]
    )
