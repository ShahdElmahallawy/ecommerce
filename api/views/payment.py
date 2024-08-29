import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from api.selectors import list_payments, get_payment
from api.serializers.payment import PaymentSerializer
from api.services import update_payment, create_payment, delete_payment


logger = logging.getLogger(__name__)


class PaymentListView(APIView):
    """
    API view for listing the user's payments."""

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handle GET requests to list the user's payments.

        Returns:
            Response object containing the list of payments.
        """
        logger.info(f"User {request.user} requested their payments")
        payments = list_payments(request.user)
        serializer = PaymentSerializer(payments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentCreateView(APIView):
    """
    API view for creating a payment."""

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to create a payment.

        Returns:
            Response object containing the created payment data.
        """
        logger.info(f"User {request.user} requested to create a payment")
        data = request.data
        serializer = PaymentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        payment = create_payment(serializer.validated_data, request.user)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PaymentDetailView(APIView):
    """
    API view for retrieving, updating, and deleting a payment.

    Returns:
        Response object containing the payment data.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        logger.info(f"User {request.user} requested a payment")
        payment = get_payment(kwargs.get("payment_id"), request.user)
        if not payment:
            logger.error(f"Payment not found for user {request.user}")
            return Response(
                {"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentUpdateView(APIView):
    """
    API view for updating a payment."""

    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, *args, **kwargs):
        """
        Handle PATCH requests to update a payment.

        Returns:
            Response object containing the updated payment data."""
        logger.info(f"User {request.user} requested to update a payment")
        payment = get_payment(kwargs.get("payment_id"), request.user)
        if not payment:
            logger.error(f"Payment not found for user {request.user}")
            return Response(
                {"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = PaymentSerializer(payment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        payment = update_payment(serializer.validated_data, payment)
        serializer = PaymentSerializer(payment)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PaymentDeleteView(APIView):
    """
    API view for deleting a payment.

    Returns:
        Response object with no content.
    """

    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        logger.info(f"User {request.user} requested to delete a payment")
        payment = get_payment(kwargs.get("payment_id"), request.user)
        if not payment:
            logger.error(f"Payment not found for user {request.user}")
            return Response(
                {"detail": "Payment not found."}, status=status.HTTP_404_NOT_FOUND
            )
        delete_payment(payment)
        return Response(status=status.HTTP_204_NO_CONTENT)
