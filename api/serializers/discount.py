from rest_framework import serializers
from api.models.discount import Discount


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
