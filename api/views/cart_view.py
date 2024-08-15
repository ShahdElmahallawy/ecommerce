from api.serializers.cart_serializer import CartSerializer
from api.models.cart import Cart
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from api.service.cart_service import add_product_to_cart, remove_product_from_cart, calculate_cart_total, checkout_cart
from rest_framework.response import Response
from rest_framework import status

class CartView(viewsets.ModelViewSet):
    """ViewSet of cart.
    
    Fields:
    - queryset: query set of cart
    - serializer_class: serializer
    - endpoints:  add product - delete product - list all products - total price - checkout - update payment 
    """
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Add a product to the cart.
        """
        cart = add_product_to_cart(request.user, request.data.get('product_id'), request.data.get('quantity'))
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def destroy(self, request, *args, **kwargs):
        """
        Remove a product from the cart.
        """
        remove_product_from_cart(request.user, kwargs.get('pk'))
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def list(self, request, *args, **kwargs):
        """
        List all products in the cart.
        """
        cart = request.user.cart
        serializer = self.get_serializer(cart)
        return Response(serializer.data)
    
    def total_price(self, request, *args, **kwargs):
        """
        Calculate the total price of all items in the cart.
        """
        total = calculate_cart_total(request.user)
        return Response({'total': total})
    
    def checkout(self, request, *args, **kwargs):
        """
        Checkout the cart.
        """
        response = checkout_cart(request.user)
        return Response(response)
    
    
    
    

