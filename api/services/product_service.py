from api.selectors.product_selector import get_all_products, get_product_by_id
from api.models.product import Product
import logging

def list_products():
    """
    Service to list all products.
    """
    return get_all_products()

def retrieve_product(product_id):
    """
    Service to retrieve a single product by ID.
    """
    return get_product_by_id(product_id)


def update_product(product_id, user, data):
    """
    Service to update a product if the user is the creator.
    """
    product = get_product_by_id(product_id)
    if product and product.created_by == user:
        for key, value in data.items():
            setattr(product, key, value)
        product.save()
        return product
    else:
        logging.warning(f'Product with ID {product_id} not found or user is not the creator.')
    return None

def delete_product(product_id, user):
    """
    Service to delete a product.
    """
    product = get_product_by_id(product_id)
    if product and product.created_by == user:
        product.delete()
        return True
    else:
        logging.warning(f'Product with ID {product_id} not found or user is not the creator.')
    return False
