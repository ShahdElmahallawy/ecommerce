from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken


class CustomJWTAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)

        if validated_token.get("type") == "otp":
            raise InvalidToken("OTP tokens cannot be used for this request.")

        user = self.get_user(validated_token)

        if user.password_changed_at and validated_token["iat"] < int(
            user.password_changed_at.timestamp()
        ):
            raise InvalidToken(
                "Password has been changed recently. Please log in again."
            )

        return validated_token


class OTPAuthentication(JWTAuthentication):
    def get_validated_token(self, raw_token):
        validated_token = super().get_validated_token(raw_token)

        if validated_token.get("type") != "otp":
            raise InvalidToken("This endpoint requires an OTP token.")

        return validated_token
