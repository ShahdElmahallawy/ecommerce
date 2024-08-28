from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from api.selectors.order import get_order_by_id_and_user, get_orders_by_user

from api.services.order import cancel_order, create_order, mark_order_as_delivered

from api.serializers.order import OrderSerializer

from api.models.payment import Payment

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
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderListView(APIView):
    def get(self, request):
        orders = get_orders_by_user(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        payment_method_id = request.data.get("payment_method")
        items_data = request.data.get("items", [])

        try:
            payment_method = Payment.objects.get(id=payment_method_id)
        except Payment.DoesNotExist:
            return Response(
                {"error": "Invalid payment method."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not items_data:
            return Response(
                {"error": "Order must contain at least one item."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = create_order(user, payment_method, items_data)
            serializer = OrderSerializer(order)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            logger.error(f"Failed to create order for user {user}: {str(e)}")
            return Response(
                {"error": "Failed to create order."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class OrderDeliverView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk):
        response_data, success = mark_order_as_delivered(pk, request.user)
        if success:
            return Response(response_data, status=status.HTTP_200_OK)
        return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
