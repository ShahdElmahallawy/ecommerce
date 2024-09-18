from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from api.models.cart import Cart
from api.models.product import Product
from api.models.cart_item import CartItem
from api.selectors.product import get_product_by_id


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Enter a valid quantity greater than 0")
        return value


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    quantity = serializers.IntegerField()

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Enter a valid quantity greater than 0")
        return value


class ProductSimpleSerializer(serializers.ModelSerializer):
    """Serializer for a product"""

    class Meta:
        model = Product
        fields = ["id", "name", "price"]
        read_only_fields = ["id", "name", "price"]


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = CartItem
        fields = ["id", "product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["id", "user", "items", "total_price"]

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])
