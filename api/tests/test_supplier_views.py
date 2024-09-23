import pytest
from api.models import Supplier
from django.urls import reverse


@pytest.fixture
def supplier():
    return Supplier.objects.create(name="Test Supplier", email="testsupplier@email.com")


@pytest.mark.django_db
def test_list_suppliers_view(client, supplier):
    url = reverse("supplier-list")
    response = client.get(url)
    assert response.status_code == 200
    assert response.data[0]["id"] == 1


@pytest.mark.django_db
def test_create_supplier_view(supplier, api_admin_auth):
    url = reverse("supplier-create")
    response = api_admin_auth.post(
        url, {"name": "Test Supplier", "email": "testsupplier@email.com"}
    )
    assert response.status_code == 201
    assert response.data["name"] == "Test Supplier"

    # invalid name
    response = api_admin_auth.post(
        url, {"name": "a", "email": "testsupplier@email.com"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_supplier_view(supplier, api_admin_auth):
    url = reverse("supplier-update", args=[1])
    response = api_admin_auth.patch(url, {"name": "Updated Supplier"})
    assert response.status_code == 200
    assert response.data["name"] == "Updated Supplier"

    # invalid name
    response = api_admin_auth.patch(
        url, {"name": "a", "email": "testsupplier@email.com"}
    )
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_supplier_view(supplier, api_admin_auth):
    url = reverse("supplier-delete", args=[1])
    response = api_admin_auth.delete(url)
    assert Supplier.objects.count() == 0


@pytest.mark.django_db
def test_supplier_detail_view(supplier, client):
    url = reverse("supplier-detail", args=[1])
    response = client.get(url)
    assert response.status_code == 200
    assert response.data["name"] == "Test Supplier"
    assert response.data["email"] == "testsupplier@email.com"
