from api.selectors.product_variant import (
    get_product_variant_by_id,
    list_product_variants,
    get_product_variant_by_id_for_edit,
    list_product_variants_by_product_id,
)
from api.models.product import Product, ProductVariant


def create_product_variant(data):
    """
    Service to create a product variant.
    """
    options = data.pop("options")
    product_variant = ProductVariant.objects.create(**data)
    product_variant.options.set(options)
    return product_variant


def update_product_variant(product_variant, data):
    """
    Service to update a product variant.
    """
    if "options" in data:
        options = data.pop("options")
        product_variant.options.set(options)
    for key, value in data.items():
        setattr(product_variant, key, value)
    product_variant.save()
    return product_variant


def delete_product_variant(product_variant):
    """
    Service to delete a product variant.
    """

    product_variant.delete()
