from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.selectors.settled import get_seller_order_items

# from api.services.settled import categorize_orders_by_date
from api.serializers.order_item import OrderItemSerializer


class SellerOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        seller = request.user

        order_items = get_seller_order_items(seller)

        # categorized_orders = categorize_orders_by_date(order_items)
        serializer = OrderItemSerializer(order_items, many=True)

        return Response(serializer.data)
