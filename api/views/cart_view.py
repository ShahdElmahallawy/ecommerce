from api.serializers.cart_serializer import CartSerializer
from rest_framework.permissions import IsAuthenticated
from api.service.cart_service import (
    add_product_to_cart,
    remove_product_from_cart,
    calculate_cart_total,
    checkout_cart,
)
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView


class CreateCartView(APIView):
    """
    Add a product to the cart.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = add_product_to_cart(
            request.user, request.data.get("product_id"), request.data.get("quantity")
        )
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class DeleteCartView(APIView):
    """
    Remove a product from the cart.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, pk):
        remove_product_from_cart(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)


class ListCartView(APIView):
    """
    List all products in the cart.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = request.user.cart
        serializer = CartSerializer(cart)
        return Response(serializer.data)


class TotalPriceCartView(APIView):
    """
    Calculate the total price of all items in the cart.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        total = calculate_cart_total(request.user)
        return Response({"total": total})


class CheckoutCartView(APIView):
    """
    Checkout the cart.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        response = checkout_cart(request.user)
        return Response(response)
