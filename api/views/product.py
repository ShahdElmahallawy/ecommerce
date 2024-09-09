from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from api.selectors.product import (
    get_product_by_id,
    list_products,
    get_product_by_id_for_edit,
)
from api.serializers.product import ProductSerializer, ProductDetailSerializer
from api.services.product import create_product, update_product, delete_product
from api.permissions import IsAdminOrSeller
from rest_framework.permissions import IsAuthenticated
from logging import getLogger
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from api.filters.product import ProductFilter
from api.filters.product import ProductRatingFilter

logger = getLogger(__name__)


class ProductListView(GenericAPIView):
    """
    View to list all products.
    """

    def get_queryset(self):
        queryset = list_products()
        queryset = ProductRatingFilter.filter_rating(
            queryset, self.request.query_params
        )

        return queryset

    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category"]
    search_fields = ["name"]
    ordering_fields = ["price", "created_at", "rating"]
    filterset_class = ProductFilter

    def get(self, request):
        """
        Handle GET request to list all products.
        """
        logger.info("User requested to view all products")
        filtered_products = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filtered_products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDetailView(APIView):
    """
    View to get details of a product.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to get details of a product.
        """
        logger.info(f"User requested to view product {kwargs['product_id']}")
        product = get_product_by_id(kwargs["product_id"])
        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductDetailSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductCreateView(APIView):
    """
    View to create a product.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def post(self, request):
        """
        Handle POST request to create a product.
        """
        logger.info("User requested to create a product")
        serializer = ProductSerializer(
            data=request.data, context={"user": request.user}
        )
        serializer.is_valid(raise_exception=True)
        product = create_product(serializer.validated_data)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ProductUpdateView(APIView):
    """
    View to update a product.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def patch(self, request, product_id):
        """
        Handle PATCH request to update a product.
        """
        logger.info(f"User requested to update product {product_id}")
        product = get_product_by_id_for_edit(product_id, request.user)
        if not product:
            logger.error(f"Product {product_id} not found, failed to update")
            return Response(
                {"detail": "No available product found."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = update_product(serializer.validated_data, product)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProductDeleteView(APIView):
    """
    View to delete a product.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def delete(self, request, product_id):
        """
        Handle DELETE request to delete a product.
        """

        product = get_product_by_id_for_edit(product_id, request.user)
        if not product:
            logger.error(f"Product {product_id} not found, failed to delete")
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        delete_product(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
