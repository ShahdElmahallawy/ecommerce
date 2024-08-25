from api.models import Wishlist, WishlistItem


def get_wishlist_by_user(user):
    """Get the wishlist of a user or create one if it doesn't exist"""
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    return wishlist


def get_wishlist_items(wishlist):
    """Get the items in a wishlist"""
    return WishlistItem.objects.filter(wishlist=wishlist)


def get_wishlist_item(wishlist, product):
    """Get a wishlist item"""
    return WishlistItem.objects.filter(wishlist=wishlist, product=product).first()
