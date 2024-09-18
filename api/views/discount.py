from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from api.serializers.discount import DiscountSerializer
from api.services.discount import create_discount
from api.models.discount import Discount
import logging

logger = logging.getLogger(__name__)


class DiscountCreateView(APIView):

    # permission_classes = [IsAuthenticated]

    def post(self, request):

        user = request.data.get("user")
        code = request.data.get("code")
        discount_percentage = request.data.get("discount_percentage")

        serializer = DiscountSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)

        if not user or not code or not discount_percentage:
            return Response(
                {"error": "user, code, and discount_percentage are required fields."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        discount = create_discount(serializer.validated_data)

        serializer = DiscountSerializer(discount)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class DiscountListView(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        from api.models.user import User

        discounts = Discount.objects.all()
        serializer = DiscountSerializer(discounts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
