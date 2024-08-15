from api.models.product import Product

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
        return None
    
def get_products_by_category(category_name):
    """
    Returns products filtered by category name.
    """
    return Product.objects.filter(category__name=category_name)

def get_all_products_with_details():
    """
    Returns all products with related data prefetched.
    """
    return Product.objects.prefetch_related('category', 'reviews').all()
