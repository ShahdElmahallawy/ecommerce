from api.models import Product


def get_product_by_id(product_id):
    """
    Selector to get a product by its ID.

    Returns:
        The product with the given ID.
    """
    try:
        product = Product.objects.select_related("category").prefetch_related("reviews").get(id=product_id)
    except Product.DoesNotExist:
        return None

    return product


def list_products():
    """
    Selector to list products.

    Returns:
        A queryset of products.
    """
    return Product.objects.select_related("category").prefetch_related("reviews").all()


def get_product_by_id_for_edit(product_id, user):
    """
    Selector to get a product by its ID.

    Returns:
        The product with the given ID.
    """
    try:
        if user.is_staff:
            product = Product.objects.get(id=product_id)
        else:
            product = Product.objects.get(id=product_id, created_by=user)
    except Product.DoesNotExist:
        return None

    return product
