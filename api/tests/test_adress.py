import pytest

from api.models.user import User
from api.models.address import Address
from api.serializers.address import AddressSerializer
from django_countries.fields import Country


@pytest.mark.django_db
def test_create_address_without_default():
    user = User.objects.create_user(email="testuser@example.com", name="Test User")

    address = Address.objects.create(
        user=user,
        street_address="123 Main St",
        apartment_address="Apt 1",
        country="US",
        zip="12345",
        address_type="billing",
    )

    assert address.default is True


@pytest.mark.django_db
def test_create_second_address(user):

    Address.objects.create(
        user=user,
        street_address="123 Ahmad St",
        apartment_address="October",
        country=Country(code="US"),
        zip="12345",
        address_type="home",
        default=True,
    )

    address2 = Address.objects.create(
        user=user,
        street_address="456 Paymob St",
        apartment_address="Maadi",
        country=Country(code="US"),
        zip="67890",
        address_type="work",
    )

    assert address2.default is False


@pytest.mark.django_db
def test_setting_new_address_as_default(user):
    address1 = Address.objects.create(
        user=user,
        street_address="123 Ahmad St",
        apartment_address="October",
        country=Country(code="US"),
        zip="12345",
        address_type="home",
        default=True,
    )

    address2 = Address.objects.create(
        user=user,
        street_address="456 Paymob St",
        apartment_address="Maadi",
        country=Country(code="US"),
        zip="67890",
        address_type="work",
        default=True,
    )

    address1.refresh_from_db()
    assert address1.default is False
    assert address2.default is True


# serializer tests
@pytest.mark.django_db
def test_serializer_valid_data(user):
    data = {
        "user": user.id,
        "street_address": "123 Ahmad St",
        "apartment_address": "October",
        "country": "US",
        "zip": "12345",
        "address_type": "home",
        "default": True,
    }

    serializer = AddressSerializer(data=data)
    assert serializer.is_valid()
    address = serializer.save()

    assert address.street_address == "123 Ahmad St"
    assert address.default is True


@pytest.mark.django_db
def test_serializer_invalid_zip_code(user):
    data = {
        "user": user.id,
        "street_address": "123 Ahmad St",
        "apartment_address": "Ocober",
        "zip": "string not int",
        "address_type": "home",
        "default": True,
    }

    serializer = AddressSerializer(data=data)
    assert not serializer.is_valid()
    assert "zip" in serializer.errors


@pytest.mark.django_db
def test_serializer_set_default_address(user):

    Address.objects.create(
        user=user,
        street_address="123 Ahmad St",
        apartment_address="October",
        country=Country(code="US"),
        zip="12345",
        address_type="home",
        default=True,
    )

    data = {
        "user": user.id,
        "street_address": "456 Paymob St",
        "apartment_address": "Maadi",
        "country": "US",
        "zip": "67890",
        "address_type": "work",
        "default": True,
    }

    serializer = AddressSerializer(data=data)
    assert serializer.is_valid()
    address = serializer.save()

    assert address.default is True
    old_default_address = Address.objects.get(street_address="123 Ahmad St")
    assert old_default_address.default is False
