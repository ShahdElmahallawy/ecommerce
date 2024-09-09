from api.models import Product


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
    product.delete()
    return None
