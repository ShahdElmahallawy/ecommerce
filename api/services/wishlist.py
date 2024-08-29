from api.models import WishlistItem
from api.selectors.wishlist import get_wishlist_by_user, get_wishlist_item
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError


from django.db import IntegrityError


def add_item_to_wishlist(wishlist, product):
    """Add an item to a wishlist"""
    try:
        wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=product)
        wishlist = get_wishlist_by_user(wishlist.user)
        return wishlist
    except IntegrityError:
        raise ValidationError({"detail": "Item already exists in wishlist"})


def delete_item_from_wishlist(wishlist, item_id):
    """Delete an item from a wishlist"""
    try:
        item = get_wishlist_item(wishlist, item_id)
        item.delete()
        wishlist = get_wishlist_by_user(wishlist.user)
        return wishlist
    except WishlistItem.DoesNotExist:
        raise ValidationError({"detail": "Item does not exist in wishlist"})


def clear_wishlist(wishlist):
    """Clear all items from a wishlist"""
    WishlistItem.objects.filter(wishlist=wishlist).delete()
    wishlist = get_wishlist_by_user(wishlist.user)
    return wishlist
