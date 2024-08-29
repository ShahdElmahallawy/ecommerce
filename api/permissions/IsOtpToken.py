from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.exceptions import PermissionDenied


class IsOtpToken(BasePermission):
    """
    Custom permission to check if the token is an OTP token.
    """

    def has_permission(self, request, view):
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            return False

        try:
            token = auth_header.split(" ")[1]
            access_token = AccessToken(token)

            if access_token["type"] != "otp":
                raise PermissionDenied("Invalid token type.")
        except Exception as e:
            raise PermissionDenied(f"Token validation failed: {str(e)}")

        return True
