from rest_framework import serializers

from api.models.order import Order

from api.serializers.order_item import OrderItemSerializer
from rest_framework.exceptions import ValidationError


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "user",
            "payment_method",
            "status",
            "total_price",
            "items",
            "created_at",
            "updated_at",
        ]


class OrderCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [
            "user",
            "payment_method",
        ]

        read_only_fields = ["user"]

    payment_method = serializers.IntegerField()


class OrderCreateWithDiscountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["user", "payment_method", "discount_code"]

        read_only_fields = ["user"]

    payment_method = serializers.IntegerField()
    discount_code = serializers.CharField()

    def validate_discount_code(self, value):
        if len(str(value)) <= 4:
            raise ValidationError("code must be more than 4 charachters")
        return value
