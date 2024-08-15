from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated 

from api.selector.order import get_order_by_id_and_user, get_orders_by_user
from api.service.order import cancel_order

from api.serializers.order import OrderSerializer

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
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListView(APIView):
    permission_classes = [IsAuthenticated]  
    def get(self, request):
        orders = get_orders_by_user(request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
