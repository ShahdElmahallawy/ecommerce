from rest_framework import serializers
from api.models.discount import Discount
from rest_framework.exceptions import ValidationError


class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = [
            "id",
            "user",
            "code",
            "discount_percentage",
            "start_date",
            "end_date",
            "is_active",
        ]

    def validate_code(self, value):
        if len(str(value)) <= 4:
            raise ValidationError("code must be more than 4 charachters")
        return value
