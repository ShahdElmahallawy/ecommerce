from api.models.product import Variant, VariantOption


def get_variants():
    """
    Get all variants.
    """
    return Variant.objects.all()


def get_variant_by_id(variant_id):
    """
    Get a variant by its ID.
    """
    try:
        return Variant.objects.get(id=variant_id)
    except Variant.DoesNotExist:
        return None


def get_options():
    """
    Get all options.
    """
    return VariantOption.objects.all()


def get_variant_option_by_id(option_id):
    """
    Get an option by its ID.
    """
    try:
        return VariantOption.objects.get(id=option_id)
    except VariantOption.DoesNotExist:
        return None
