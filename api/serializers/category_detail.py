from rest_framework import serializers
from api.models.category import Category
from api.serializers.product_serializer import Product


class CategoryDetailSerializer(serializers.ModelSerializer):
    featured_product = Product()

    class Meta:
        model = Category
        fields = ["id", "name", "featured_product"]
