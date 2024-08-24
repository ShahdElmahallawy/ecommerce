from rest_framework import serializers
from datetime import datetime
from api.models import Payment


class ExpiryDateField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(value, "%m/%y").date().replace(day=1)
        except ValueError:
            raise serializers.ValidationError("Expiry date must be in MM/YY format.")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "user", "pan", "bank_name", "expiry_date", "cvv", "card_type"]

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    expiry_date = ExpiryDateField()
