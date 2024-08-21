from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser ,IsAuthenticated

from api.selector.category import (
    get_all_categories,
    get_category_by_id,
    get_products_by_category,
)
from api.service.category import update_category, delete_category

from api.serializers.category import CategorySerializer
from api.serializers.category_detail import CategoryDetailSerializer
from api.serializers.product_serializer import ProductSerializer


class CategoryListView(APIView):
    def get(self, request):
        categories = get_all_categories()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDetailView(APIView):
    def get(self,request, pk):
        category = get_category_by_id(pk)
        serializer = CategoryDetailSerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryUpdateView(APIView):
    permission_classes = [IsAdminUser]  
    def put(self, request, pk):
        updated_category = update_category(pk, request.data)
        serializer = CategorySerializer(updated_category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryDeleteView(APIView):
    permission_classes = [IsAdminUser]
    def delete(self, request, pk):
        delete_category(pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class CategoryProductListView(APIView):
    permission_classes = [IsAuthenticated]  
    
    def get(self, request, category_pk):
        category = get_category_by_id(category_pk)
        products = get_products_by_category(category)
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
