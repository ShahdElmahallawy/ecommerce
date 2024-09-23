from rest_framework import serializers
from api.models import Store, Inventory, Product
from api.validators.user_input import only_alphanumeric


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ["id", "name", "seller", "is_default_shipping", "location"]
        read_only_fields = ["id", "seller"]

    is_default_shipping = serializers.BooleanField(required=False, default=False)

    def validate_name(self, value):
        only_alphanumeric(value)

        return value

    def validate_location(self, value):
        only_alphanumeric(value)
        return value


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image", "price"]
        read_only_fields = ["id"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "product", "stock"]
        read_only_fields = ["id", "seller"]

    product = SimpleProductSerializer(read_only=True)


class StoreDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "name",
            "seller",
            "is_default_shipping",
            "location",
            "inventory",
        ]
        read_only_fields = ["id", "seller"]

    inventory = InventorySerializer(many=True, read_only=True)
