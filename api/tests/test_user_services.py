import pytest
from django.contrib.auth import get_user_model
from api.services import create_user

User = get_user_model()


@pytest.mark.django_db
def test_create_user():
    user_data = {
        "email": "amr@example.com",
        "name": "amr",
        "password": "password123",
    }

    tokens = create_user(user_data)

    user = User.objects.get(email="amr@example.com")
    assert user.name == "amr"
    assert user.check_password("password123")
    assert "refresh" in tokens
    assert "access" in tokens
