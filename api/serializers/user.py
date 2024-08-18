from django.contrib.auth import get_user_model

from rest_framework import serializers
from api.selectors import get_user_by_reset_token


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for user register.

    Attributes:
        password: The user's password (write-only).
    """

    password = serializers.CharField(write_only=True)

    class Meta:
        model = get_user_model()
        fields = ["email", "password", "name"]

    def validate(self, data):
        """
        Validates the provided data.


        Returns:
            data: The validated data.
        """
        if data.get("password"):
            if len(data.get("password")) < 8:
                raise serializers.ValidationError(
                    "Password must be at least 8 characters long."
                )

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


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        """
        Validate that the email exists in the database.
        """
        if not get_user_model().objects.filter(email=value).exists():
            raise serializers.ValidationError("No user with this email found.")
        return value


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
