from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from api.selectors.order import get_order_by_id_and_user, get_orders_by_user
from api.services.order import create_order_session
from api.selectors.user import get_user_by_email
from api.services.order import (
    cancel_order,
    create_order_from_cart,
    mark_order_as_delivered,
    create_order_from_cart_multiple_stores,
)
from api.serializers.order import (
    OrderSerializer,
    OrderCreateSerializer,
    OrderCreateWithDiscountSerializer,
)

import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


import logging

logger = logging.getLogger(__name__)


class OrderCancelView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        response_data, success = cancel_order(pk, request.user)
        if success:
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class OrderTrackView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_order_by_id_and_user(pk, request.user)
        serializer = OrderSerializer(order)
        if serializer.data["user"] == None:
            return Response(
                {"detail": "No order Found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = get_orders_by_user(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDeliverView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        response_data, success = mark_order_as_delivered(pk, request.user)
        if success:
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class OrderCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info(f"Creating order for {request.user.email}")
        serializer = OrderCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        payment_method = serializer.validated_data["payment_method"]

        try:
            order = create_order_from_cart(user=user, payment_method=payment_method)
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


class OrderCreateViewWithDiscount(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = OrderCreateWithDiscountSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        payment_method = serializer.validated_data["payment_method"]
        discount_code = serializer.validated_data["discount_code"]

        try:
            order = create_order_from_cart(
                user=user, payment_method=payment_method, discount_code=discount_code
            )
        except ValueError as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        order_serializer = OrderSerializer(order)
        return Response(order_serializer.data, status=status.HTTP_201_CREATED)


# using stripe session
class OrderCreateViewAmr(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = None
        if request.data.get("discount_code"):
            serializer = OrderCreateWithDiscountSerializer(data=request.data)
        else:
            serializer = OrderCreateSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        user = request.user
        payment_method = serializer.validated_data["payment_method"]

        try:
            session = create_order_session(request, user, payment_method)
            return Response(session, status=status.HTTP_200_OK)

        except Exception as err:
            return Response({"details": str(err)}, status=status.HTTP_400_BAD_REQUEST)


class StripeWebhookView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        endpoint_secret = settings.WEBHOOK_SECRET_KEY

        try:
            event = stripe.Webhook.construct_event(
                payload=payload, sig_header=sig_header, secret=endpoint_secret
            )
        except ValueError as e:
            return Response({"error": "Invalid payload"}, status=400)
        except stripe.error.SignatureVerificationError as e:
            return Response({"error": "Invalid signature"}, status=400)

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            handle_checkout_session_completed(session)

        return Response({"status": "success"}, status=status.HTTP_200_OK)


class OrderPaymentResponseView(APIView):
    def get(self, request):
        payment_status = request.query_params.get("status")
        if payment_status == "success":
            return Response(
                {"message": "Payment successful"}, status=status.HTTP_200_OK
            )
        return Response(
            {"message": "Payment failed"}, status=status.HTTP_400_BAD_REQUEST
        )


def handle_checkout_session_completed(session):
    logger.info(f"Handling checkout session completed for session {session.id}")
    payment_method = session.metadata.get("payment_method")
    discount_code = session.metadata.get("discount_code")
    user_email = session.customer_email
    user = get_user_by_email(user_email)

    try:
        order = create_order_from_cart(user, payment_method, discount_code)
        logger.info(f"Order created for user {user_email}")
    except ValueError as e:
        logger.error(f"Error creating order for user {user_email}: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    logger.info(f"Order created for user final {user_email}")
    return Response({"order_id": order.id}, status=status.HTTP_200_OK)
