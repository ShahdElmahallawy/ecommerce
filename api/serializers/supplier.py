from rest_framework import serializers
from api.models import Supplier
from api.validators.user_input import only_characters


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = ["id", "name", "email"]
        read_only_fields = ["id"]

    def validate_name(self, value):
        if len(value.strip()) < 4:
            raise serializers.ValidationError("Name must be at least 4 characters.")

        only_characters(value)

        return value
