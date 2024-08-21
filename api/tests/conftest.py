import pytest

from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from api.models.payment import Payment


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_data():
    return {
        "email": "amr@example.com",
        "name": "Amr Test",
        "password": "testpassword123",
    }


@pytest.fixture
def user(db, user_data):
    User = get_user_model()
    user = User.objects.create_user(**user_data)
    return user


@pytest.fixture
def admin(db, user_data):
    User = get_user_model()
    user = User.objects.create_superuser(**user_data)
    return user


@pytest.fixture
def api_client_auth(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def api_admin_auth(admin):
    client = APIClient()
    client.force_authenticate(user=admin)
    return client

@pytest.fixture
def payment(user):
    return Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )
