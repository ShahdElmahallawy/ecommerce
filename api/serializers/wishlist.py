from rest_framework import serializers
from api.models import Wishlist, WishlistItem, Product


class ProductSimpleSerializer(serializers.ModelSerializer):
    """Serializer for a product"""

    class Meta:
        model = Product
        fields = ["id", "name", "price"]
        read_only_fields = ["id", "name", "price"]


class WishlistItemSerializer(serializers.ModelSerializer):
    """Serializer for a wishlist item"""

    class Meta:
        model = WishlistItem
        fields = ["id", "product"]

    id = serializers.IntegerField(read_only=True)
    product = ProductSimpleSerializer()


class WishlistSerializer(serializers.ModelSerializer):
    """Serializer for the Wishlist model"""

    class Meta:
        model = Wishlist
        fields = ["id", "user", "items", "results"]

    items = WishlistItemSerializer(many=True)
    results = serializers.SerializerMethodField()

    def get_results(self, obj):
        return obj.items.count()


class WishlistItemCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating a wishlist item"""

    class Meta:
        model = WishlistItem
        fields = ["product"]
