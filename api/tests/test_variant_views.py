import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from api.tests.factories import VariantFactory, VariantOptionFactory


@pytest.fixture
def variant():
    variant = VariantFactory()
    variant_option = VariantOptionFactory(variant=variant)
    return variant, variant_option


@pytest.mark.django_db
def test_create_variant(api_admin_auth):
    data = {"name": "Test Variant"}
    url = reverse("variant-create")
    response = api_admin_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["name"] == data["name"]


@pytest.mark.django_db
def test_create_option(api_admin_auth):
    variant = VariantFactory()
    data = {"value": "Test Option", "variant": variant.id}
    url = reverse("variant-option-create")
    response = api_admin_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["value"] == data["value"]
    assert response.data["variant"]["id"] == variant.id


def test_update_variant(api_admin_auth, variant):
    variant, _ = variant
    data = {"name": "Updated Variant"}
    url = reverse("variant-update", args=[variant.id])
    response = api_admin_auth.patch(url, data)
    print(response.data)
    assert response.status_code == 200
    assert response.data["name"] == data["name"]

    url = reverse("variant-update", args=[999])
    response = api_admin_auth.patch(url, data)
    assert response.status_code == 404


def test_update_option(api_admin_auth, variant):
    _, variant_option = variant
    data = {"value": "Updated Option"}
    url = reverse("variant-option-update", args=[variant_option.id])
    response = api_admin_auth.patch(url, data)
    assert response.status_code == 200
    assert response.data["value"] == data["value"]

    url = reverse("variant-option-update", args=[999])
    response = api_admin_auth.patch(url, data)
    assert response.status_code == 404


def test_delete_variant(api_admin_auth, variant):
    variant, _ = variant
    url = reverse("variant-delete", args=[variant.id])
    response = api_admin_auth.delete(url)
    assert response.status_code == 204

    response = api_admin_auth.delete(url)
    assert response.status_code == 404


def test_delete_option(api_admin_auth, variant):
    _, variant_option = variant
    url = reverse("variant-option-delete", args=[variant_option.id])
    response = api_admin_auth.delete(url)
    assert response.status_code == 204

    response = api_admin_auth.delete(url)
    assert response.status_code == 404


def test_variant_detail(api_admin_auth, variant):
    variant, _ = variant
    url = reverse("variant-detail", args=[variant.id])
    response = api_admin_auth.get(url)
    assert response.status_code == 200
    assert response.data["name"] == variant.name

    url = reverse("variant-detail", args=[999])
    response = api_admin_auth.get(url)
    assert response.status_code == 404


def test_option_detail(api_admin_auth, variant):
    _, variant_option = variant
    url = reverse("variant-option-detail", args=[variant_option.id])
    response = api_admin_auth.get(url)
    assert response.status_code == 200
    assert response.data["value"] == variant_option.value
    assert response.data["variant"]["id"] == variant_option.variant.id

    url = reverse("variant-option-detail", args=[999])
    response = api_admin_auth.get(url)
    assert response.status_code == 404
