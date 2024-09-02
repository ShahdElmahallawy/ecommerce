from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.selectors.cart import get_cart_by_user
from api.services.cart import (
    add_to_cart,
    remove_from_cart,
    clear_cart,
    update_cart_item,
)
from api.serializers.cart import (
    CartSerializer,
    CartItemUpdateSerializer,
    CartItemCreateSerializer,
)
from api.permissions import IsAuthenticated


class AddToCartView(APIView):
    """Add a product to cart"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CartItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = add_to_cart(
            request.user,
            serializer.validated_data["product"],
            serializer.validated_data["quantity"],
        )
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)


class RemoveFromCartView(APIView):
    """Remove a product from cart"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        cart = remove_from_cart(request.user, item_id)
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


class ClearCartView(APIView):
    """Clear the cart"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        cart = clear_cart(request.user)
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


class UpdateCartItemView(APIView):
    """Update a cart item"""

    permission_classes = [IsAuthenticated]

    def patch(self, request, item_id):
        serializer = CartItemUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cart = update_cart_item(
            request.user, item_id, serializer.validated_data["quantity"]
        )
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)


class CartView(APIView):
    """Get the cart for the user"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        cart = get_cart_by_user(request.user)
        cart_serializer = CartSerializer(cart)
        return Response(cart_serializer.data, status=status.HTTP_200_OK)
