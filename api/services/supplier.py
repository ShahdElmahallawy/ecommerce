from api.selectors.supplier import get_supplier_by_id, get_all_suppliers
from api.models import Supplier
from rest_framework.exceptions import ValidationError


def create_supplier(data):
    return Supplier.objects.create(**data)


def update_supplier(supplier_id, data):
    try:
        supplier = get_supplier_by_id(supplier_id)
    except Supplier.DoesNotExist:
        raise ValidationError("Supplier not found")
    for key, value in data.items():
        setattr(supplier, key, value)
    supplier.save()
    return supplier


def delete_supplier(supplier_id):
    try:
        supplier = get_supplier_by_id(supplier_id)
    except Supplier.DoesNotExist:
        raise ValidationError("Supplier not found")
    supplier.delete()
    return supplier
