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


class WishlistItemCreateSerializer(serializers.Serializer):
    """Serializer for creating a wishlist item"""

    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        """Validate the product id"""
        try:
            # TODO: Replace this with product selector once implemented
            product = Product.objects.get(pk=value)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist")
        return product

    class Meta:
        model = WishlistItem
        fields = ["product_id"]
