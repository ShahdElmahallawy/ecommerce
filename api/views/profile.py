from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from api.services import update_profile
from api.selectors import get_user_profile
from api.serializers import ProfileSerializer


class ProfileDetailView(APIView):
    """
    API view for updating and retrieving the user's profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to retrieve the user's profile.

        Returns:
            Response object containing the profile data.
        """
        profile = get_user_profile(request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProfileUpdateView(APIView):
    """
    API view for updating the user's profile.
    """

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests to update the user's profile.

        Returns:
            Response object containing the updated profile data.
        """
        profile = get_user_profile(request.user)
        updated_profile = update_profile(profile, request.data)
        serializer = ProfileSerializer(updated_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
