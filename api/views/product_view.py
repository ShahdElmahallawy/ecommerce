from api.serializers.product_serializer import ProductSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.services.product_service import (
    list_products,
    retrieve_product,
    update_product,
    delete_product,
)
from rest_framework.views import APIView


class CreateProductView(APIView):
    """
    View to create a new product.
    """

    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = ProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProductsView(APIView):
    """
    List all products.
    """

    permission_classes = []

    def get(self, request):
        products = list_products()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)


class RetrieveProductView(APIView):
    """
    Retrieve a single product by ID.
    """

    permission_classes = []

    def get(self, request, pk):
        product = retrieve_product(pk)
        if product is None:
            return Response(
                {"detail": "No active product found with the given ID."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class UpdateProductView(APIView):
    """
    Update a product by ID.
    """

    permission_classes = [IsAdminUser]

    def put(self, request, pk):
        product = update_product(pk, request.user, request.data)
        if product is None:
            return Response(
                {
                    "detail": "No active product found with the given ID, or user is not the creator."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = ProductSerializer(product)
        return Response(serializer.data)


class DeleteProductView(APIView):
    """
    Delete a product by ID.
    """

    permission_classes = [IsAdminUser]

    def delete(self, request, pk):
        success = delete_product(pk, request.user)
        if not success:
            return Response(
                {
                    "detail": "No active product found with the given ID, or user is not the creator."
                },
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
