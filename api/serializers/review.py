from rest_framework import serializers
from api.models import Review
from api.selectors.product import get_product_by_id

from django.contrib.auth import get_user_model
from api.validators.user_input import only_alphanumeric

User = get_user_model()


class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "name"]
        read_only_fields = ["id", "email", "name"]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["id", "user", "product", "rating", "text"]
        read_only_fields = ["id", "user", "product"]

    user = UserSimpleSerializer(read_only=True)

    def validate_rating(self, value):
        if value < 0 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value

    def validate(self, data):
        if self.context.get("product_id"):
            data["product"] = get_product_by_id(self.context["product_id"])
            if not data.get("product"):
                raise serializers.ValidationError("Product not found.")
        return data

    def validate_text(self, value):
        if value and value.strip():
            only_alphanumeric(value)
        return value
