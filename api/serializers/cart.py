from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from api.models import CartItem, Cart, Product
from api.selectors.product import get_product_by_id


class CartItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["product", "quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be greater than 0")
        return value

    def validate_product(self, value):
        product = get_product_by_id(value.id)
        if product is None:
            raise ValidationError("Product does not exist")
        return product


class CartItemUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ["quantity"]

    def validate_quantity(self, value):
        if value <= 0:
            raise ValidationError("Quantity must be greater than 0")
        return value


class ProductSimpleSerializer(serializers.ModelSerializer):
    """Serializer for a product"""

    class Meta:
        model = Product
        fields = ["id", "name", "price"]
        read_only_fields = ["id", "name", "price"]


class CartItemerializer(serializers.ModelSerializer):
    product = ProductSimpleSerializer()

    class Meta:
        model = CartItem
        fields = ["product", "quantity"]


class CartSerializer(serializers.ModelSerializer):
    items = CartItemCreateSerializer(many=True)

    class Meta:
        model = Cart
        fields = ["user", "items", "total_price"]

    total_price = serializers.SerializerMethodField()

    def get_total_price(self, cart):
        return sum([item.product.price * item.quantity for item in cart.items.all()])
