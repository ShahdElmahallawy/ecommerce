from statistics import mean
from rest_framework import serializers
from api.models import Product
from api.selectors.store import get_stock_in_default_store
from api.serializers.review import ReviewSerializer
from api.validators.user_input import only_alphanumeric


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price",
            "count",
            "created_by",
            "category",
            "currency",
            "description",
            "image",
            "rating",
            "num_reviews",
            "created_at",
            "stock",
        ]
        read_only_fields = ["created_by", "created_at"]

    rating = serializers.FloatField(read_only=True)
    num_reviews = serializers.IntegerField(read_only=True)
    created_at = serializers.DateTimeField(read_only=True, format="%Y-%m-%d")
    stock = serializers.SerializerMethodField()

    def get_stock(self, product):
        return get_stock_in_default_store(product)

    def validate(self, data):
        # if price := data.get("price") and price < 0:
        if "price" in data and data["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative.")

        if "count" in data and data["count"] < 0:
            raise serializers.ValidationError("Count cannot be negative.")

        if self.context.get("user"):
            data["created_by"] = self.context["user"]
        return data

    def validate_name(self, value):
        only_alphanumeric(value)
        return value

    def validate_description(self, value):
        if value and value.strip():
            only_alphanumeric(value)
        return value


class ProductDetailSerializer(ProductSerializer):
    class Meta(ProductSerializer.Meta):
        fields = ProductSerializer.Meta.fields + ["reviews", "num_reviews"]

    reviews = ReviewSerializer(many=True, read_only=True)
