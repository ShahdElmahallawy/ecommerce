from api.models.product import ProductVariant


def get_product_variant_by_id(product_variant_id):
    """
    Selector to get a product variant by its ID.
    """
    try:
        product_variant = ProductVariant.objects.get(id=product_variant_id)
    except ProductVariant.DoesNotExist:
        return None

    return product_variant


def list_product_variants():
    """
    Selector to list product variants.
    """
    product_variants = ProductVariant.objects.all()
    return product_variants


def get_product_variant_by_id_for_edit(product_variant_id, user):
    """
    Selector to get a product variant by its ID.
    """
    try:
        if user.is_staff:
            product_variant = ProductVariant.objects.get(id=product_variant_id)
        else:
            product_variant = ProductVariant.objects.get(
                id=product_variant_id, product__created_by=user
            )
    except ProductVariant.DoesNotExist:
        return None

    return product_variant


def list_product_variants_by_product_id(product_id):
    """
    Selector to list product variants by product ID.
    """
    product_variants = ProductVariant.objects.filter(product_id=product_id)
    return product_variants
