from api.serializers.product_serializer import ProductSerializer
from api.models.product import Product
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from api.service.product_service import list_products, retrieve_product, update_product, delete_product

class ProductView(viewsets.ModelViewSet):

    """ViewSet of product.
    
    Fields:
    - queryset: query set of product
    - serializer_class: serializer
    - endpoints:  list all products - get_product_details -update product - delete product 
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Override to use service for fetching active products.
        """
        return list_products()
    
    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve a product, ensuring it's from an active user.
        """
        product = retrieve_product(kwargs.get('pk'))
        if product is None:
            return Response({'detail': 'No active product found with the given ID.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        """
        Update a product, ensuring it's done by the creator and the creator is active.
        """
        product = update_product(kwargs.get('pk'), request.user, request.data)
        if product is None:
            return Response({'detail': 'No active product found with the given ID, or user is not the creator.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(product)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Delete a product, ensuring it's done by the creator and the creator is active.
        """
        success = delete_product(kwargs.get('pk'), request.user)
        if not success:
            return Response({'detail': 'No active product found with the given ID, or user is not the creator.'}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)

   