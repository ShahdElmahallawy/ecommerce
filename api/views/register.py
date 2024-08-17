from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.services import create_user
from api.serializers import RegisterSerializer


class UserRegisterView(APIView):
    """
    API view for user register.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user register.

        Returns:
            Response object containing the JWT token pair or validation errors.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = create_user(serializer.validated_data)
        return Response(tokens, status=status.HTTP_201_CREATED)
