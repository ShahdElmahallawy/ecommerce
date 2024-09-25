from rest_framework import serializers
from api.models import Store, Inventory, Product
from api.selectors.product import get_product_by_id_for_edit
from api.selectors.store import get_store_by_seller


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "image", "price"]
        read_only_fields = ["id"]


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["id", "product", "stock", "store"]
        read_only_fields = ["id", "store"]

    product = SimpleProductSerializer(read_only=True)


class InventoryCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ["product", "stock", "store"]

    product = serializers.IntegerField()
    stock = serializers.IntegerField()
    store = serializers.IntegerField()

    def validate_product(self, value):
        if not value:
            raise serializers.ValidationError("Product is required.")
        product = get_product_by_id_for_edit(value, self.context["request"].user)
        if not product:
            raise serializers.ValidationError("No available product found.")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock must be a positive integer.")
        return value

    def validate_store(self, value):
        if not value:
            raise serializers.ValidationError("Store is required.")
        if not get_store_by_seller(self.context["request"].user, value):
            raise serializers.ValidationError("Store not found.")
        return value
