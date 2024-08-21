from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from api.selectors.wishlist import (
    get_wishlist_by_user,
)
from api.services.wishlist import (
    add_item_to_wishlist,
    delete_item_from_wishlist,
    clear_wishlist,
)
from api.serializers import (
    WishlistSerializer,
    WishlistItemSerializer,
    WishlistItemCreateSerializer,
)


class WishlistListView(APIView):
    """Api view for the wishlist"""

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Handle GET request for user's wishlist
        Returns:
            Response object containing the wishlist data.
        """
        wishlist = get_wishlist_by_user(request.user)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishlistDeleteView(APIView):
    """Api view for clearing a wishlist"""

    permission_classes = [IsAuthenticated]

    def delete(self, request):
        """Handle DELETE request to clear a wishlist
        Returns:
            Response object containing the cleared wishlist data.
        """
        wishlist = get_wishlist_by_user(request.user)
        wishlist = clear_wishlist(wishlist)
        serializer = WishlistSerializer(wishlist)
        return Response(serializer.data, status=status.HTTP_200_OK)


class WishlistItemCreateView(APIView):
    """Api view for creating a wishlist item"""

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """Handle POST request to create a wishlist item
        Returns:
            Response object containing the created wishlist item data.
        """
        wishlist = get_wishlist_by_user(request.user)
        serializer = WishlistItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        wishlist_item = add_item_to_wishlist(
            wishlist, serializer.validated_data.get("product")
        )
        serializer = WishlistItemSerializer(wishlist_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class WishlistItemDeleteView(APIView):
    """Api view for deleting a wishlist item"""

    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        """Handle DELETE request to delete a wishlist item
        Returns:
            Response object containing the deleted wishlist item data.
        """
        wishlist = get_wishlist_by_user(request.user)
        success = delete_item_from_wishlist(wishlist, product_id)
        if not success:
            return Response(
                {"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND
            )
        return Response(status=status.HTTP_204_NO_CONTENT)
