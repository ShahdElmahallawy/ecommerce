from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.serializers import RegisterSerializer


class UserRegistrationView(APIView):
    """
    API view for user registration.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.

        Returns:
            Response object containing the JWT token pair or validation errors.
        """
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
