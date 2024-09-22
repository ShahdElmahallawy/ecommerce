from api.models.product import Variant, VariantOption


def create_variant(data):
    """
    Create a variant.
    """
    variant = Variant.objects.create(**data)
    return variant


def create_option(data):
    """
    Create an option.
    """
    option = VariantOption.objects.create(**data)
    return option


def update_variant(variant, data):
    """
    Update a variant.
    """
    for key, value in data.items():
        setattr(variant, key, value)
    variant.save()
    return variant


def update_option(option, data):
    """
    Update an option.
    """
    for key, value in data.items():
        setattr(option, key, value)
    option.save()
    return option


def delete_variant(variant):
    """
    Delete a variant.
    """
    variant.delete()


def delete_option(option):
    """
    Delete an option.
    """
    option.delete()
