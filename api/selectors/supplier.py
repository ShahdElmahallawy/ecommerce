from api.models import Supplier


def get_supplier_by_id(supplier_id):
    return Supplier.objects.get(id=supplier_id)


def get_all_suppliers():
    return Supplier.objects.all()
