from django.contrib.auth import get_user_model

from rest_framework import serializers


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
