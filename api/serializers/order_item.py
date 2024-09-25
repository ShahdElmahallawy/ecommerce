from rest_framework import serializers
from api.models.order_item import OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "quantity", "unit_price", "user", "settled_status"]

    user = serializers.SerializerMethodField()
    settled_status = serializers.SerializerMethodField()

    def get_user(self, instance):
        return instance.order.user.id

    def get_settled_status(self, instance):
        return instance.order.settled_status
