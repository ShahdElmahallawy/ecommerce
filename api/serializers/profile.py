from django.contrib.auth import get_user_model

from rest_framework import serializers

from api.models import Profile


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
        fields = ["user", "phone", "preferred_currency"]

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
