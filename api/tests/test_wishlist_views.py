import pytest
from rest_framework import status
from api.models import Product, Wishlist, WishlistItem, Category


from django.urls import reverse


@pytest.fixture
def product():
    return Product.objects.create(name="Test Product", price=100.0)


@pytest.fixture
def wishlist(user):
    return Wishlist.objects.create(user=user)


@pytest.fixture
def wishlist_item(wishlist, product):
    return WishlistItem.objects.create(wishlist=wishlist, product=product)


@pytest.mark.django_db
def test_wishlist_list_view(api_client_auth, wishlist):
    url = reverse("wishlist-list")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert "id" in response.data
    assert "user" in response.data
    assert "items" in response.data
    assert "results" in response.data


@pytest.mark.django_db
def test_wishlist_item_create_view(api_client_auth, product):
    data = {"product": product.id}
    url = reverse("wishlist-item-create")
    response = api_client_auth.post(url, data)

    assert response.status_code == status.HTTP_201_CREATED
    assert WishlistItem.objects.filter(product=product).exists()


@pytest.mark.django_db
def test_wishlist_item_create_view_fail(api_client_auth):
    data = {"product": 2}
    url = reverse("wishlist-item-create")
    response = api_client_auth.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_wishlist_item_delete_view(api_client_auth, wishlist_item):
    url = reverse("wishlist-item-delete", kwargs={"item_id": 1})
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert not WishlistItem.objects.filter(id=wishlist_item.id).exists()


@pytest.mark.django_db
def test_wishlist_delete_view_fail(api_client_auth, wishlist, wishlist_item):
    url = reverse("wishlist-item-delete", kwargs={"item_id": 2})
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert WishlistItem.objects.filter(wishlist=wishlist).count() == 1


@pytest.mark.django_db
def test_wishlist_delete_view(api_client_auth, wishlist, wishlist_item):
    url = reverse("wishlist-clear")
    response = api_client_auth.delete(url)
    assert response.status_code == status.HTTP_200_OK
    assert WishlistItem.objects.filter(wishlist=wishlist).count() == 0
