from rest_framework import serializers
from datetime import datetime
from api.models import Payment
from api.validators.user_input import only_alphanumeric


class ExpiryDateField(serializers.DateField):
    def to_internal_value(self, value):
        try:
            return datetime.strptime(value, "%m/%y").date().replace(day=1)
        except ValueError:
            raise serializers.ValidationError("Expiry date must be in MM/YY format.")


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "pan",
            "bank_name",
            "expiry_date",
            "cvv",
            "card_type",
            "default",
        ]

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    id = serializers.IntegerField(read_only=True)
    expiry_date = ExpiryDateField()

    def validate_pan(self, value):
        if len(str(value)) != 16:
            raise serializers.ValidationError("PAN must be 16 digits.")
        return value

    def validate_cvv(self, value):
        if len(str(value)) != 3:
            raise serializers.ValidationError("CVV must be 3 digits.")
        return value

    def validate_bank_name(self, value):
        only_alphanumeric(value)

        return value
