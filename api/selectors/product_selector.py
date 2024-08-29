from api.models.product import Product
import logging

logger = logging.getLogger(__name__)


def get_all_products():
    """
    Returns all products where the 'created_by' user has not been deleted.
    """
    return Product.objects.exclude(created_by__isnull=True)


def get_product_by_id(product_id):
    """
    Returns a single product matched by ID or None if not found.
    """
    try:
        return Product.objects.get(id=product_id)
    except Product.DoesNotExist:
        logger.warning(f"Product with ID {product_id} not found")
        return None


def get_products_by_category(category_name):
    """
    Returns products filtered by category name.
    """
    return Product.objects.filter(category__name=category_name)


def get_all_products_with_details():
    """
    Returns all products with related data.
    """
    return Product.objects.select_related("category").all()
