from django.contrib.auth import get_user_model

from rest_framework import serializers
from api.selectors import get_user_by_email
from api.validators.user_input import only_alphanumeric


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user register.

    Attributes:
        password: The user's password (write-only).
    """

    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name", "confirm_password", "user_type"]

    def validate_name(self, value):
        """
        Validate the provided name.

        Returns:
            value: The validated name.
        """
        if len(value.strip()) < 4:
            raise serializers.ValidationError("Name must be at least 4 characters.")

        only_alphanumeric(value)

        return value

    def validate_password(self, value):
        """
        Validate the provided password.

        Returns:
            value: The validated password.
        """
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters.")
        return value

    def validate(self, data):
        """
        Validate the provided data.

        Returns:
            data: The validated data.
        """
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        data.pop("confirm_password")

        return data


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    class Meta:
        fields = ["email", "password"]

    def validate(self, data):
        """
        Validate the provided data.

        Returns:
            data: The validated data.
        """
        if not data.get("email") or not data.get("password"):
            raise serializers.ValidationError(
                {"error": "Email and password are required."}
            )

        user = get_user_by_email(data["email"])

        if not user or not user.check_password(data["password"]):
            raise serializers.ValidationError({"error": "Invalid email or password."})

        data["user"] = user
        return data


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    class Meta:
        fields = ["refresh"]

    def validate(self, data):
        """
        Validate the provided data.

        Returns:
            data: The validated data.
        """
        if not data.get("refresh"):
            raise serializers.ValidationError({"error": "Refresh token is required."})

        return data


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ["email"]


class PasswordResetSerializer(serializers.Serializer):
    new_password = serializers.CharField(min_length=8)
    confirm_new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        """
        Validate that the new passwords match and the token is valid.
        """
        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        return data


class OTPVerificationSerializer(serializers.Serializer):
    """
    Serializer for verifying OTP code.
    """

    otp_code = serializers.CharField(max_length=6)

    def validate_otp_code(self, value):
        """
        Validate that the OTP code is correct for the user.
        """
        user = self.context["user"]
        if user.otp_code != value:
            raise serializers.ValidationError("Invalid OTP code.")

        user.otp_code = None
        user.save(update_fields=["otp_code"])

        return value


class UpdateUserPasswordSerializer(serializers.Serializer):
    """
    Serializer for updating user password.
    """

    current_password = serializers.CharField()
    new_password = serializers.CharField(min_length=8)
    confirm_new_password = serializers.CharField(min_length=8)

    def validate(self, data):
        """
        Validate that the new passwords match and the current password is correct.
        """
        user = self.context["user"]

        if not user.check_password(data["current_password"]):
            raise serializers.ValidationError({"error": "Invalid current password."})

        if data["new_password"] != data["confirm_new_password"]:
            raise serializers.ValidationError({"error": "Passwords do not match."})

        return data
