from rest_framework import serializers
from api.models.category import Category
from api.serializers.product import Product
class CategoryDetailSerializer(serializers.ModelSerializer):
    products = Product(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'products']
