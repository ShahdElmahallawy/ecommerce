from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from api.models.order import Order
from api.serializers.order import OrderSerializer

class OrderCancelView(APIView):
    def post(self  , request, pk):
        order = get_object_or_404(order, pk=pk, user=request.user)
        if order.status == 'pending':
            order.status = 'cancelled'
            order.save()
            return Response({'status': 'Order cancelled'}, status=status.HTTP_200_OK)
        return Response({'error': 'Order cannot be cancelled'}, status=status.HTTP_400_BAD_REQUEST)

class OrderTrackView(APIView):
    def get(self, request, pk):
        order = get_object_or_404(order, pk=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)

class OrderListView(APIView):
    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)