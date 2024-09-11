# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from api.services.top import get_top_selling_products_for_sellers, get_top_rated_products_for_sellers
# from rest_framework.permissions import IsAuthenticated

# class TopSellingProductsView(APIView):
#     permission_classes = [IsAuthenticated] 
#     def get(self, request):
#         limit = int(request.query_params.get('limit', 10))
#         try:
#             result = get_top_selling_products_for_sellers(limit)
#             if len(result) !=0:
#                 return Response(result, status=status.HTTP_200_OK)
#             else:
#                 return Response("No items",status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class TopRatedProductsView(APIView):
#     permission_classes = [IsAuthenticated] 

#     def get(self, request):
#         limit = int(request.query_params.get('limit', 10))
#         try:
#             top_rated_products = get_top_rated_products_for_sellers(limit=int(limit))
#             if len(top_rated_products) !=0:
#                 return Response(top_rated_products, status=status.HTTP_200_OK)
#             else:
#                 return Response("No items",status=status.HTTP_404_NOT_FOUND)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.services.top import get_top_selling_products_for_sellers, get_top_rated_products_for_sellers, get_top_selling_products, get_top_rated_products
from api.models import Product
from api.serializers import ProductSerializer

class TopSellingProductsView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        seller_id = request.query_params.get('seller_id')
        
        result = get_top_selling_products(seller_id, limit)
        
        if isinstance(result, list): 
            return Response(ProductSerializer(Product.objects.filter(id__in=result), many=True).data)
        else: 
            serialized_result = {}
            for seller_id, product_ids in result.items():
                serialized_result[seller_id] = ProductSerializer(Product.objects.filter(id__in=product_ids), many=True).data
            return Response(serialized_result)

class TopRatedProductsView(APIView):
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        seller_id = request.query_params.get('seller_id')
        
        result = get_top_rated_products(seller_id, limit)
        
        if isinstance(result, list): 
            return Response(ProductSerializer(Product.objects.filter(id__in=result), many=True).data)
        else: 
            serialized_result = {}
            for seller_id, product_ids in result.items():
                serialized_result[seller_id] = ProductSerializer(Product.objects.filter(id__in=product_ids), many=True).data
            return Response(serialized_result)