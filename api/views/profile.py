import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

from api.services import update_profile
from api.selectors import get_user_profile
from api.serializers import ProfileSerializer

logger = logging.getLogger(__name__)


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
        logger.info(f"User {request.user} requested their profile")
        profile = get_user_profile(request.user)
        if not profile:
            logger.error(f"Profile not found for user {request.user}")
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )
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
        logger.info(f"User {request.user} requested to update their profile")
        profile = get_user_profile(request.user)
        if not profile:
            logger.error(f"Profile not found for user {request.user}")
            return Response(
                {"detail": "Profile not found."}, status=status.HTTP_404_NOT_FOUND
            )
        updated_profile = update_profile(profile, request.data)
        serializer = ProfileSerializer(updated_profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
