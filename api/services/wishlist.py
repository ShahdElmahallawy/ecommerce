from api.models import WishlistItem
from api.selectors.wishlist import get_wishlist_by_user, get_wishlist_item
from django.db import IntegrityError
from rest_framework.exceptions import ValidationError
from logging import getLogger
from django.db import IntegrityError

logger = getLogger(__name__)


def add_item_to_wishlist(user, product):
    """Add an item to a wishlist"""
    try:
        wishlist = get_wishlist_by_user(user)
        wishlist_item = WishlistItem.objects.create(wishlist=wishlist, product=product)
        wishlist = get_wishlist_by_user(user)
        return wishlist
    except IntegrityError:
        logger.error(f"Item already exists in wishlist for user {user}, failed to add")
        raise ValidationError({"detail": "Item already exists in wishlist"})


def delete_item_from_wishlist(user, item_id):
    """Delete an item from a wishlist"""
    try:
        item = get_wishlist_item(user, item_id)
        item.delete()
        wishlist = get_wishlist_by_user(user)
        return wishlist
    except WishlistItem.DoesNotExist:
        logger.error(
            f"Item does not exist in wishlist for user {user}, failed to delete"
        )
        raise ValidationError({"detail": "Item does not exist in wishlist"})


def clear_wishlist(user):
    """Clear all items from a wishlist"""
    WishlistItem.objects.filter(wishlist__user=user).delete()
    wishlist = get_wishlist_by_user(user)
    return wishlist
