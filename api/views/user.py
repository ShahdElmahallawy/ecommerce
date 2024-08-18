from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.services import create_user, generate_reset_password_token, reset_user_password
from api.selectors import get_user_by_reset_token, get_user_by_email
from api.serializers import (
    RegisterSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


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


class PasswordResetRequestView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_by_email(serializer.validated_data["email"])
        generate_reset_password_token(user, request)
        return Response(
            {"detail": "Password reset link sent."}, status=status.HTTP_200_OK
        )


class PasswordResetView(APIView):
    def post(self, request, token, *args, **kwargs):
        user = get_user_by_reset_token(token)
        if not user:
            return Response(
                {"detail": "Invalid or expired token."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = PasswordResetSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        reset_user_password(user, serializer.validated_data["new_password"])
        return Response(
            {"detail": "Password has been reset successfully."},
            status=status.HTTP_200_OK,
        )
