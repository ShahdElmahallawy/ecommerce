from django.contrib.auth import get_user_model

from rest_framework import serializers
from api.selectors import get_user_by_email


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
        fields = ["email", "password", "name", "confirm_password"]

    def validate_name(self, value):
        """
        Validate the provided name.

        Returns:
            value: The validated name.
        """
        if len(value.strip()) < 4:
            raise serializers.ValidationError("Name must be at least 4 characters.")

        if not all(char.isalnum() or char.isspace() for char in value):
            raise serializers.ValidationError("Name must be alphanumeric.")

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
            raise serializers.ValidationError("Passwords do not match.")

        data.pop("confirm_password")

        return data

    def create(self, validated_data):
        """
        Creates a new user with the provided validated data.


        Returns:
            user: The created user instance.
        """
        user = get_user_model().objects.create_user(
            email=validated_data.get("email"),
            password=validated_data.get("password"),
            name=validated_data.get("name"),
        )
        return user


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
            raise serializers.ValidationError("Email and password are required.")

        user = get_user_by_email(data["email"])
        if user and not user.check_password(data["password"]):
            raise serializers.ValidationError("Invalid email or password.")

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
            raise serializers.ValidationError("Refresh token is required.")

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
            raise serializers.ValidationError("Passwords do not match.")

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

        return value
