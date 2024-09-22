from api.models.product import Variant, VariantOption
from api.tests.factories import VariantFactory, VariantOptionFactory
import pytest

from api.services.variant import (
    create_variant,
    create_option,
    update_variant,
    update_option,
    delete_variant,
    delete_option,
)


@pytest.fixture
def variant(db):
    variant = VariantFactory()
    variant_option = VariantOptionFactory(variant=variant)
    return variant, variant_option


@pytest.mark.django_db
def test_create_variant():
    data = {"name": "Test Variant"}
    result = create_variant(data)
    assert result.name == data["name"]


@pytest.mark.django_db
def test_create_option():
    variant = VariantFactory()
    data = {"value": "Test Option", "variant": variant}
    result = create_option(data)
    assert result.value == data["value"]
    assert result.variant == variant


def test_update_variant(variant):
    variant, _ = variant
    data = {"name": "Updated Variant"}
    result = update_variant(variant, data)
    assert result.name == data["name"]


def test_update_option(variant):
    _, variant_option = variant
    data = {"value": "Updated Option"}
    result = update_option(variant_option, data)
    assert result.value == data["value"]


def test_delete_variant(variant):
    variant, _ = variant
    delete_variant(variant)
    assert Variant.objects.count() == 0


def test_delete_option(variant):
    _, variant_option = variant
    delete_option(variant_option)
    assert VariantOption.objects.count() == 0
