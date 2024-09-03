from statistics import mean
from rest_framework import serializers
from api.models import Product


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
        ]
        read_only_fields = ["created_by"]

    rating = serializers.SerializerMethodField()

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if not reviews:
            return 0
        return mean([review.rating for review in reviews])

    def validate(self, data):
        if "price" in data and data["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative.")

        if "count" in data and data["count"] < 0:
            raise serializers.ValidationError("Count cannot be negative.")

        if self.context.get("user"):
            data["created_by"] = self.context["user"]
        return data
