from api.selector.cart_selector import get_cart_by_user, get_cart_item, get_cart_items

def add_product_to_cart(user, product_id, quantity):
    """
    Service to add a product to a user's cart. Adjusts quantity if the product is already in the cart.
    """
    cart = get_cart_by_user(user)
    cart_item = get_cart_item(cart, product_id)
    if cart_item:
        cart_item.quantity += quantity
        cart_item.save()
    else:
        from api.models import CartItems, Product
        product = Product.objects.get(pk=product_id)
        CartItems.objects.create(cart=cart, product_id=product, quantity=quantity)
    return cart

def remove_product_from_cart(user, product_id):
    """
    Service to remove a product from the cart.
    """
    cart = get_cart_by_user(user)
    cart_item = get_cart_item(cart, product_id)
    if cart_item:
        cart_item.delete()

def calculate_cart_total(user):
    """
    Service to calculate the total price of all items in the cart.
    """
    cart = get_cart_by_user(user)
    total = 0
    for item in get_cart_items(cart):
        total += item.quantity * item.product_id.price
    return total

def checkout_cart(user):
    """
    Service to handle checkout logic. Placeholder for actual implementation.
    """
    total = calculate_cart_total(user)
    return {'status': 'Checkout complete', 'total': total}
