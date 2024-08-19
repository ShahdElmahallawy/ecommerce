import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from api.models import Profile


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
def api_client_auth(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client
