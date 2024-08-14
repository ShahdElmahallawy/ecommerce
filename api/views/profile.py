from rest_framework import generics, permissions
from api.serializers import ProfileSerializer


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    API view for retrieving and updating the user's profile.
    """

    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ["get", "patch"]

    def get_object(self):
        """
        Retrieve the profile of the currently authenticated user.

        Returns:
            Profile: Profile associated with the current user.
        """
        return self.request.user.profile
