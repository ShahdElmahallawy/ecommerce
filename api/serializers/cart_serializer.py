from api.models.cart_items import CartItems
from rest_framework import serializers

class CartItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItems
        fields = ['product_id', 'quantity', 'cart']

        