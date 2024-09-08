import pytest
from api.selectors.supplier import get_supplier_by_id, get_all_suppliers
from api.models import Supplier


@pytest.fixture
def supplier(db):
    supplier = Supplier.objects.create(
        name="Test Supplier", email="testsupplier@example.com"
    )
    return supplier


@pytest.mark.django_db
def test_get_supplier_by_id(supplier):
    supplier = get_supplier_by_id(1)
    assert supplier.id == 1


@pytest.mark.django_db
def test_get_supplier_fail():
    with pytest.raises(Supplier.DoesNotExist):
        get_supplier_by_id(1)


@pytest.mark.django_db
def test_get_all_suppliers(supplier):
    suppliers = get_all_suppliers()
    assert suppliers.count() == 1
    assert suppliers[0].id == 1
    assert suppliers[0].name == "Test Supplier"
    assert suppliers[0].email == "testsupplier@example.com"
