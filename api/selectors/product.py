from api.models import Product
from django.db.models import Avg, Count


def get_product_by_id(product_id):
    """
    Selector to get a product by its ID.

    Returns:
        The product with the given ID.
    """
    try:
        product = (
            Product.objects.select_related("category")
            .prefetch_related("reviews")
            .exclude(is_deleted=True)
            .get(id=product_id)
        )
    except Product.DoesNotExist:
        return None

    return product


def list_products():
    """
    Selector to list products.

    Returns:
        A queryset of products.
    """
    products = (
        Product.objects.select_related("category")
        .prefetch_related("reviews")
        .exclude(is_deleted=True)
        .annotate(rating=Avg("reviews__rating"))
        .annotate(num_reviews=Count("reviews"))
    )
    return products


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
