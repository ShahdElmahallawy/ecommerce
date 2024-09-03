from api.models import Wishlist, WishlistItem
from logging import getLogger

logger = getLogger(__name__)


def get_wishlist_by_user(user):
    """Get a wishlist by user"""
    wishlist = (
        Wishlist.objects.filter(user=user).prefetch_related("items__product").first()
    )
    if not wishlist:
        logger.info("Creating a new wishlist for user %s", user)
        wishlist = Wishlist.objects.create(user=user)
    return wishlist


def get_wishlist_item(user, id):
    """Get a wishlist item"""
    return WishlistItem.objects.get(wishlist__user=user, id=id)


def get_wishlist_item_by_product(user, product):
    """Get a wishlist item by product"""
    return WishlistItem.objects.get(wishlist__user=user, product=product)
