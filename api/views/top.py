from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.top import (
    get_top_selling_products_for_sellers,
    get_top_rated_products_for_sellers,
    get_top_selling_products,
    get_top_rated_products,
)
from api.models import Product
from api.serializers import ProductSerializer

from rest_framework.permissions import IsAuthenticated


class TopSellingProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        seller_id = request.query_params.get("seller_id")

        result = get_top_selling_products(seller_id, limit)

        if isinstance(result, list):
            return Response(
                ProductSerializer(Product.objects.filter(id__in=result), many=True).data
            )
        else:
            serialized_result = {}
            for seller_id, product_ids in result.items():
                serialized_result[seller_id] = ProductSerializer(
                    Product.objects.filter(id__in=product_ids), many=True
                ).data
            return Response(serialized_result)


class TopRatedProductsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        limit = int(request.query_params.get("limit", 10))
        seller_id = request.query_params.get("seller_id")

        result = get_top_rated_products(seller_id, limit)

        if isinstance(result, list):
            return Response(
                ProductSerializer(Product.objects.filter(id__in=result), many=True).data
            )
        else:
            serialized_result = {}
            for seller_id, product_ids in result.items():
                serialized_result[seller_id] = ProductSerializer(
                    Product.objects.filter(id__in=product_ids), many=True
                ).data
            return Response(serialized_result)
