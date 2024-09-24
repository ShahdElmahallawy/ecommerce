from api.models.address import Address
from django.shortcuts import get_object_or_404


def get_all_addresses_for_user(user):
    return Address.objects.filter(user=user)


def get_address_by_id(user, pk):
    return get_object_or_404(Address, pk=pk, user=user)
