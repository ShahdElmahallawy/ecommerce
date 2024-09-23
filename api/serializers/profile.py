from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.models import Profile
from api.validators.user_input import only_digits


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model appearing in profile
    """

    class Meta:
        model = get_user_model()
        fields = ["email", "name", "user_type"]


class ProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for the Profile model.

    Attributes:
    user: A nested serializer for the associated user.
    """

    user = UserProfileSerializer()

    class Meta:
        model = Profile
        fields = ["user", "address", "phone", "preferred_currency"]

    def validate_phone(self, value):
        """
        Validate the provided phone number.
        """
        if len(value) != 11:
            raise serializers.ValidationError("Phone number must be 11 digits.")
        only_digits(value)
        return value

    def update(self, instance, validated_data):
        """
        Update the profile and the associated user's information.
        """
        user_data = validated_data.pop("user", None)
        if user_data:
            user_serializer = UserProfileSerializer(
                instance=instance.user, data=user_data, partial=True
            )
            if user_serializer.is_valid():
                user_serializer.save()

        return super().update(instance, validated_data)
