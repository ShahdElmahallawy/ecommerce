from api.models import Product
from django.utils import timezone


def create_product(validated_data):
    """
    Service to create a product.

    Returns:
        The created product.
    """
    product = Product.objects.create(**validated_data)

    return product


def update_product(data, product):
    """
    Service to update a product.

    Returns:
        The updated product.
    """
    for key, value in data.items():
        setattr(product, key, value)
    product.save(update_fields=data.keys())

    return product


def delete_product(product):
    """
    Service to delete a product.

    Returns:
        None
    """
    product.is_deleted = True
    product.deleted_at = timezone.now()
    product.save(update_fields=["is_deleted", "deleted_at"])
    return None
