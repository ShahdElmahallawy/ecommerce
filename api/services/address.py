from api.models.address import Address
from api.selectors.address import get_address_by_id


def create_address( data):
    address = Address.objects.create( **data)
    return address


def update_address(user, pk, data):
    address = get_address_by_id(user, pk)
    for attr, value in data.items():
        setattr(address, attr, value)
    address.save()
    return address


def delete_address(user, pk):
    address = get_address_by_id(user, pk)
    address.delete()
    return
