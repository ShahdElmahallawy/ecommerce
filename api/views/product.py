from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.selectors.product import (
    get_product_by_id,
    list_products,
    get_product_by_id_for_edit,
)
from api.serializers.product import ProductSerializer
from api.services.product import create_product, update_product, delete_product
from api.permissions import IsAdminOrSeller
from rest_framework.permissions import IsAuthenticated


class ProductListView(APIView):
    """
    View to list all products.
    """

    def get(self, request):
        products = list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class ProductDetailView(APIView):
    """
    View to get details of a product.
    """

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to get details of a product.
        """

        product = get_product_by_id(kwargs["product_id"])
        if not product:
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class ProductCreateView(APIView):
    """
    View to create a product.
    """

    permission_classes = [IsAuthenticated, IsAdminOrSeller]

    def post(self, request):
        """
        Handle POST request to create a product.
        """

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

        product = get_product_by_id_for_edit(product_id, request.user)
        if not product:
            return Response(
                {"detail": "No available found."}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = ProductSerializer(product, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        product = update_product(serializer.validated_data, product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)


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
            return Response(
                {"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND
            )
        delete_product(product)
        return Response(status=status.HTTP_204_NO_CONTENT)
