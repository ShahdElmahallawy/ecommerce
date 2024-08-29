from api.models import Wishlist, WishlistItem


def get_wishlist_by_user(user):
    wishlist, created = Wishlist.objects.get_or_create(user=user)
    if not created:
        wishlist = Wishlist.objects.prefetch_related("items__product").get(user=user)
    return wishlist


def get_wishlist_item(wishlist, id):
    """Get a wishlist item"""
    return WishlistItem.objects.get(wishlist=wishlist, id=id)
