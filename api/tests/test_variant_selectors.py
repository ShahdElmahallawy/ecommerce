import pytest

from api.selectors.variant import (
    get_variants,
    get_variant_by_id,
    get_options,
    get_variant_option_by_id,
)
from api.tests.factories import VariantFactory, VariantOptionFactory


@pytest.fixture
def variants(db):
    variant = VariantFactory()
    variant_option = VariantOptionFactory(variant=variant)
    return variant, variant_option


def test_get_variants(variants):
    variant, _ = variants
    result = get_variants()
    assert len(result) == 1


def test_get_variant_by_id(variants):
    variant, _ = variants
    result = get_variant_by_id(variant.id)
    assert result == variant

    result = get_variant_by_id(999)
    assert result is None


def test_get_options(variants):
    _, variant_option = variants
    result = get_options()
    assert len(result) == 1


def test_get_variant_option_by_id(variants):
    _, variant_option = variants
    result = get_variant_option_by_id(variant_option.id)
    assert result == variant_option

    result = get_variant_option_by_id(999)
    assert result is None
