from api.models import Wishlist, WishlistItem, Product
from api.selectors.wishlist import get_wishlist_item, get_wishlist_items


def add_item_to_wishlist(wishlist, product):
    """Add an item to a wishlist"""
    existing_item = get_wishlist_item(wishlist, product)
    if existing_item:
        return existing_item

    wishlist_item = WishlistItem(wishlist=wishlist, product=product)
    wishlist_item.save()
    return wishlist_item


def delete_item_from_wishlist(wishlist, product):
    """Delete an item from a wishlist"""
    wishlist_item = get_wishlist_item(wishlist, product)
    if wishlist_item:
        wishlist_item.delete()
        return True
    return False


def clear_wishlist(wishlist):
    """Clear all items from a wishlist"""
    WishlistItem.objects.filter(wishlist=wishlist).delete()
    return wishlist
