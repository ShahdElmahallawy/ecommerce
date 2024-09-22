import pytest
from api.models.product import ProductVariant
from api.services.product_variant import (
    create_product_variant,
    update_product_variant,
    delete_product_variant,
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
def test_create_product_variant(variant, product_variant):
    product_variant, _ = product_variant
    option = [variant[1][1], variant[1][4]]
    data = {
        "product": product_variant.product,
        "price": 200,
        "options": option,
    }
    result = create_product_variant(data)
    assert result.price == 200
    assert result.options.count() == 2


@pytest.mark.django_db
def test_update_product_variant(product_variant):
    product_variant, _ = product_variant
    data = {
        "price": 10000,
    }
    result = update_product_variant(product_variant, data)
    assert result.price == 10000


@pytest.mark.django_db
def test_delete_product_variant(product_variant):
    product_variant, _ = product_variant
    delete_product_variant(product_variant)
    assert ProductVariant.objects.count() == 0
