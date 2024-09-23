from api.selectors.product import get_product_by_id
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from api.services.product_variant import (
    create_product_variant,
    update_product_variant,
    delete_product_variant,
)
from api.selectors.product_variant import (
    get_product_variant_by_id,
    list_product_variants,
    get_product_variant_by_id_for_edit,
    list_product_variants_by_product_id,
)
from api.serializers.product_variant import (
    ProductVariantSerializer,
    ProductVariantCreateSerializer,
    ProductVariantUpdateSerializer,
)
from api.permissions import IsAdminOrSeller
from django_filters.rest_framework import DjangoFilterBackend


class ProductVariantListView(GenericAPIView):
    def get_queryset(self):
        return list_product_variants()

    permission_classes = [IsAuthenticated, IsAdminUser]
    serializer_class = ProductVariantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["product_id"]

    def get(self, request):
        filter = self.filter_queryset(self.get_queryset())
        serializer = self.serializer_class(filter, many=True)
        return Response(serializer.data)


class ProductVariantByProductListView(APIView):
    def get(self, request, product_id):
        product = get_product_by_id(product_id)
        if product is None:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        product_variants = list_product_variants_by_product_id(product_id)
        serializer = ProductVariantSerializer(product_variants, many=True)
        return Response(serializer.data)


class ProductVariantDetailView(APIView):
    def get(self, request, product_variant_id):
        product_variant = get_product_variant_by_id(product_variant_id)
        if product_variant is None:
            return Response(
                {"error": "Product variant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductVariantSerializer(product_variant)
        return Response(serializer.data)


class ProductVariantCreateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def post(self, request, product_id):
        data = request.data.copy()
        data["product"] = product_id
        serializer = ProductVariantCreateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        product_variant = create_product_variant(serializer.validated_data)
        serializer = ProductVariantSerializer(product_variant)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductVariantUpdateView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def patch(self, request, product_variant_id):
        product_variant = get_product_variant_by_id_for_edit(
            product_variant_id, request.user
        )
        if product_variant is None:
            return Response(
                {"error": "Product variant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductVariantUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product_variant = update_product_variant(
            product_variant, serializer.validated_data
        )
        serializer = ProductVariantSerializer(product_variant)
        return Response(serializer.data)


class ProductVariantDeleteView(APIView):
    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def delete(self, request, product_variant_id):
        product_variant = get_product_variant_by_id_for_edit(
            product_variant_id, request.user
        )
        if product_variant is None:
            return Response(
                {"error": "Product variant not found"}, status=status.HTTP_404_NOT_FOUND
            )
        delete_product_variant(product_variant)
        return Response(status=status.HTTP_204_NO_CONTENT)
