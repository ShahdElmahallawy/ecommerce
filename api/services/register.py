from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken


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
