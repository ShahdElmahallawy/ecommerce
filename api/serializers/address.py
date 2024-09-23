from rest_framework import serializers
from api.models.address import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id",
            "user",
            "street_address",
            "apartment_address",
            "country",
            "zip",
            "address_type",
            "default",
        ]
