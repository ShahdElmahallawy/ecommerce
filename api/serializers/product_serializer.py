from api.models.product import Product
from rest_framework import serializers

from rest_framework import serializers
from api.models.product import Product
from api.models.category import Category

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())

    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'image', 'count', 'category', 'currency', 'created_by']
