from rest_framework.permissions import BasePermission
from api.selectors.product import get_product_by_id


class IsAdminOrSeller(BasePermission):
    """
    Custom permission to allow only admin or seller to edit the product.
    """

    def has_permission(self, request, view):
        if request.user.is_staff or request.user.user_type == "seller":
            return True
        return False
