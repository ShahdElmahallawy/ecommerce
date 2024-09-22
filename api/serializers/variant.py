from rest_framework import serializers
from api.models.product import Variant, VariantOption


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = ["id", "name"]
        read_only_fields = ["id"]


class VariantOptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantOption
        fields = ["id", "variant", "value"]
        read_only_fields = ["id"]

    variant = VariantSerializer(read_only=True)


class VariantOptionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = VariantOption
        fields = ["id", "variant", "value"]
        read_only_fields = ["id"]
