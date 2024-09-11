from api.models.product import Product
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "price", "description", "image", "count", "currency"]


# from rest_framework import serializers
# from api.models import Product,User

# class ProductSerializer(serializers.ModelSerializer):
#     average_rating = serializers.FloatField()

#     class Meta:
#         model = Product
#         fields = ['id', 'name', 'price', 'description', 'average_rating']

# class SellerWithTopProductsSerializer(serializers.ModelSerializer):
#     top_products = ProductSerializer(many=True)

#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'top_products']
