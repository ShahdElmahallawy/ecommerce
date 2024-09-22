from api.models.product import ProductVariant
import pytest
from api.selectors.product_variant import (
    get_product_variant_by_id,
    list_product_variants,
    get_product_variant_by_id_for_edit,
    list_product_variants_by_product_id,
)
from api.tests.factories import (
    ProductVariantFactory,
    VariantFactory,
    VariantOptionFactory,
    UserFactory,
    ProductFactory,
)


@pytest.fixture
def variant():

    variant = [VariantFactory(name="Color"), VariantFactory(name="Size")]
    variant_option = [
        VariantOptionFactory(variant=variant[0], value="Red"),
        VariantOptionFactory(variant=variant[0], value="Blue"),
        VariantOptionFactory(variant=variant[0], value="Green"),
        VariantOptionFactory(variant=variant[1], value="Small"),
        VariantOptionFactory(variant=variant[1], value="Medium"),
        VariantOptionFactory(variant=variant[1], value="Large"),
    ]

    return variant, variant_option


@pytest.fixture
def product_variant(variant):
    variant_option = [variant[1][0], variant[1][3]]

    user = UserFactory(password=None, user_type="seller")
    product = ProductFactory(created_by=user)

    product_variant = ProductVariantFactory(product=product, price=100)
    product_variant.options.set(variant_option)
    return product_variant, user


@pytest.mark.django_db
def test_list_product_variants(product_variant):
    result = list_product_variants()
    assert result.count() == 1


@pytest.mark.django_db
def test_get_product_variant_by_id(product_variant):
    product_variant, _ = product_variant
    result = get_product_variant_by_id(product_variant.id)
    assert result == product_variant

    result = get_product_variant_by_id(100)
    assert result is None


@pytest.mark.django_db
def test_list_product_variants_by_product_id(product_variant):
    result = list_product_variants_by_product_id(product_variant[0].product.id)
    assert result.count() == 1

    result = list_product_variants_by_product_id(100)
    assert result.count() == 0


@pytest.mark.django_db
def test_get_product_variant_by_id_for_edit(product_variant):
    product_variant, user = product_variant
    result = get_product_variant_by_id_for_edit(product_variant.id, user)
    assert result == product_variant

    user2 = UserFactory(password=None, user_type="seller")
    result = get_product_variant_by_id_for_edit(product_variant.id, user2)
    assert result is None
