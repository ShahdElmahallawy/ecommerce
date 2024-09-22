import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from api.tests.factories import (
    ProductFactory,
    ProductVariantFactory,
    UserFactory,
    VariantFactory,
    VariantOptionFactory,
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
def test_list_product_variants_view(api_admin_auth, product_variant):
    url = reverse("product-variant-list")
    response = api_admin_auth.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_list_product_variants_by_product_id_view(client, product_variant):
    url = reverse(
        "product-variant-by-product-list", args=[product_variant[0].product.id]
    )
    response = client.get(url)
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_detail_product_variant_view(client, product_variant):
    url = reverse("product-variant-detail", args=[product_variant[0].id])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["id"] == product_variant[0].id

    url = reverse("product-variant-detail", args=[100])
    response = client.get(url)
    assert response.status_code == 404


@pytest.mark.django_db
def test_create_product_variant_view(variant, product_variant):
    _, user = product_variant
    api_seller_auth = APIClient()
    api_seller_auth.force_authenticate(user=user)
    url = reverse("product-variant-create", args=[product_variant[0].product.id])
    data = {
        "product": product_variant[0].product.id,
        "price": 100,
        "options": [variant[1][0].id, variant[1][3].id],
    }
    response = api_seller_auth.post(url, data)
    assert response.status_code == 201
    assert response.data["product"] == product_variant[0].product.id
    assert response.data["price"] == 100


@pytest.mark.django_db
def test_update_product_variant_view(variant, product_variant):
    _, user = product_variant
    api_seller_auth = APIClient()
    api_seller_auth.force_authenticate(user=user)
    url = reverse("product-variant-update", args=[product_variant[0].id])
    data = {
        "price": 200,
        "options": [variant[1][0].id, variant[1][3].id],
    }
    response = api_seller_auth.patch(url, data)
    assert response.status_code == 200
    assert response.data["price"] == 200


@pytest.mark.django_db
def test_update_product_variant_view(variant, product_variant):
    _, user = product_variant
    api_seller_auth = APIClient()
    api_seller_auth.force_authenticate(user=user)
    url = reverse("product-variant-update", args=[product_variant[0].id])
    data = {
        "price": 200,
        "options": [variant[1][0].id, variant[1][3].id],
    }
    response = api_seller_auth.patch(url, data)
    assert response.status_code == 200
    assert response.data["price"] == 200
    assert response.data["options"] == [variant[1][0].id, variant[1][3].id]

    user2 = UserFactory(password=None, user_type="seller")
    api_seller_auth2 = APIClient()
    api_seller_auth2.force_authenticate(user=user2)
    response = api_seller_auth2.patch(url, data)
    assert response.status_code == 404


@pytest.mark.django_db
def test_update_product_variant_view_invalid_price(variant, product_variant):
    _, user = product_variant
    api_seller_auth = APIClient()
    api_seller_auth.force_authenticate(user=user)
    url = reverse("product-variant-update", args=[product_variant[0].id])
    data = {
        "price": -200,
        "options": [variant[1][0].id, variant[1][3].id],
    }
    response = api_seller_auth.patch(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_product_variant_view(variant, product_variant):
    _, user = product_variant
    api_seller_auth = APIClient()
    api_seller_auth.force_authenticate(user=user)
    url = reverse("product-variant-delete", args=[product_variant[0].id])
    response = api_seller_auth.delete(url)
    assert response.status_code == 204
    assert response.data == None

    response = api_seller_auth.delete(url)
    assert response.status_code == 404
