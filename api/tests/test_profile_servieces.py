import pytest
from api.services import update_profile
from api.models import Profile
from api.models.address import Address


@pytest.fixture
def user_data():
    return {
        "email": "user@example.com",
        "name": "User Test",
    }


@pytest.mark.django_db
def test_update_profile(user):
    profile = Profile.objects.get(user=user)

    address = Address.objects.create(
        user=user,
        street_address="123 Paymob St",
        apartment_address="Apt 1",
        country="US",
        zip=12345,
        address_type="company",
    )

    update_data = {
        "address": address.id,
        "phone": "01234567890",
        "preferred_currency": "USD",
    }

    updated_profile = update_profile(profile, update_data)
    update = updated_profile.address
    assert update.street_address == "123 Paymob St"
    assert update.apartment_address == "Apt 1"
    assert update.country == "US"
    assert update.zip == 12345
    assert update.address_type == "company"
    assert updated_profile.phone == "01234567890"
    assert updated_profile.preferred_currency == "USD"
