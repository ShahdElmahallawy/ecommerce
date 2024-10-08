import logging

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.permissions.jwt_authentication import OTPAuthentication
from api.serializers.user import OTPVerificationSerializer, UpdateUserPasswordSerializer
from api.services import (
    create_user,
    generate_reset_password_token,
    reset_user_password,
    get_tokens_for_user,
    get_refreshed_tokens,
    generate_otp_for_user,
    update_user_password,
)
from api.selectors import get_user_by_reset_token, get_user_by_email
from api.serializers import (
    RegisterSerializer,
    LoginSerializer,
    RefreshTokenSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)


logger = logging.getLogger(__name__)


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
        logger.info(f"User registration request from {request.data.get('email')}")
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = create_user(serializer.validated_data)
        return Response(tokens, status=status.HTTP_201_CREATED)


class UserLoginView(APIView):
    """
    API view for user login.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Returns:
            Response object containing the OTP token or validation.
        """
        logger.info(f"User login request from {request.data.get('email')}")
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = generate_otp_for_user(serializer.validated_data["user"])
        return Response(token, status=status.HTTP_200_OK)


class VerifyOTPView(APIView):
    """
    API view for verifying OTP.
    """

    authentication_classes = [OTPAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for verifying OTP.

        Returns:
            Response object containing the JWT token pair or validation errors.
        """
        logger.info(f"OTP verification request from {request.data.get('otp_code')}")
        serializer = OTPVerificationSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        tokens = get_tokens_for_user(request.user)
        return Response(tokens, status=status.HTTP_200_OK)


class RefreshTokenView(APIView):
    """
    API view for token refresh.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for token refresh.

        Returns:
            Response object containing the JWT token pair or validation errors.
        """
        logger.info(f"Token refresh request from {request.data.get('refresh')}")
        serializer = RefreshTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens = get_refreshed_tokens(serializer.validated_data["refresh"])
        return Response(tokens, status=status.HTTP_200_OK)


class ForgotPasswordView(APIView):
    """
    API view for password reset request."""

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for password reset request."""
        logger.info(f"Password reset request from {request.data.get('email')}")
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_user_by_email(serializer.validated_data["email"])
        if not user:
            logger.warning(
                f"Password reset request for non-existent user {serializer.validated_data['email']}"
            )
            # For security
            return Response(
                {"detail": "Password reset link sent."}, status=status.HTTP_200_OK
            )
        generate_reset_password_token(user, request)
        return Response(
            {"detail": "Password reset link sent."}, status=status.HTTP_200_OK
        )


class PasswordResetView(APIView):
    """
    API view for resetting user password."""

    def post(self, request, token, *args, **kwargs):
        """
        Handle POST requests for resetting user password."""
        logger.info(f"Password reset request from {token}")
        user = get_user_by_reset_token(token)
        if not user:
            logger.warning(
                f"Password reset request with invalid or expired token {token}"
            )
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


class UpdatePasswordView(APIView):
    """
    API view for updating user password."""

    permission_classes = [IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests for updating user password."""
        logger.info(f"Password update request from {request.user.email}")
        serializer = UpdateUserPasswordSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        update_user_password(request.user, serializer.validated_data["new_password"])
        token = get_tokens_for_user(request.user)
        return Response(
            {
                "detail": "Password has been updated successfully.",
                "refresh": token["refresh"],
                "access": token["access"],
            },
            status=status.HTTP_200_OK,
        )
