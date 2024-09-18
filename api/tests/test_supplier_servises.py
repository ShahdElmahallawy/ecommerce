import pytest
from api.services.supplier import create_supplier, update_supplier, delete_supplier
from rest_framework.exceptions import ValidationError
from api.models import Supplier


@pytest.fixture
def supplier():
    return Supplier.objects.create(name="Test Supplier", email="testsupplier@gmail.com")


@pytest.mark.django_db
def test_create_supplier():
    supplier = create_supplier(
        {"name": "Test Supplier", "email": "testsupplier@gmail.com"}
    )
    assert supplier.id == 1
    assert supplier.name == "Test Supplier"


@pytest.mark.django_db
def test_update_supplier(supplier):
    supplier = update_supplier(supplier.id, {"name": "Updated Supplier"})
    assert supplier.name == "Updated Supplier"


@pytest.mark.django_db
def test_update_supplier_fail():

    with pytest.raises(ValidationError):
        update_supplier(1, {"name": "Updated Supplier"})


@pytest.mark.django_db
def test_delete_supplier(supplier):
    delete_supplier(supplier.id)
    assert Supplier.objects.count() == 0
    with pytest.raises(Supplier.DoesNotExist):
        Supplier.objects.get(id=supplier.id)


@pytest.mark.django_db
def test_delete_supplier_fail():
    with pytest.raises(ValidationError):
        delete_supplier(1)
