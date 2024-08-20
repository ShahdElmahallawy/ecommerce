# Draft not used yet
# Checks if the token is valid and if the password was changed after the token was issued
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.exceptions import InvalidToken
from rest_framework_simplejwt.authentication import JWTAuthentication


class CustomIsAuthenticated(IsAuthenticated):
    def has_permission(self, request):
        """
        Check if the user is authenticated and the token is valid.
        """
        if not super().has_permission(request):
            return False

        auth = JWTAuthentication()
        try:
            raw_token = auth.get_validated_token(request)
            decoded_token = auth.decode_handler(raw_token)
            iat = decoded_token.get("iat")
            if not iat:
                return False

            user = auth.get_user(raw_token)
            if user and iat < int(user.password_changed_at.timestamp()):
                raise InvalidToken(
                    "Token was issued before the password was changed, please log in again."
                )

        except:
            return False

        return True
