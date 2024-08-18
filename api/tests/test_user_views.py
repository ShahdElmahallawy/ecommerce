import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status

from api.models import Profile


@pytest.mark.django_db
def test_user_register(api_client):
    url = reverse("user-register")

    user_data = {
        "email": "amr@example.com",
        "password": "test12345",
        "name": "Amr Test",
    }

    response = api_client.post(url, user_data, format="json")

    user_model = get_user_model()
    user = user_model.objects.get(email=user_data["email"])
    profile = Profile.objects.get(user=user)
    print(response.data)

    assert response.status_code == status.HTTP_201_CREATED
    assert "refresh" in response.data
    assert "access" in response.data
    assert user is not None
    assert profile is not None
    assert user.name == user_data["name"]
    assert user.check_password(user_data["password"])


@pytest.mark.django_db
def test_user_register_with_invalid_email(api_client):
    url = reverse("user-register")

    user_data = {"email": "amr", "password": "testpassword123", "name": "Amr Test"}

    response = api_client.post(url, user_data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "email" in response.data


@pytest.mark.django_db
def test_user_register_with_missing_field(api_client):
    url = reverse("user-register")

    user_data = [
        {"password": "testpassword123", "name": "Amr Test"},
        {"email": "amr@example.com", "name": "Amr Test"},
        {
            "email": "amr@example.com",
            "password": "testpassword123",
        },
    ]

    for user in user_data:
        response = api_client.post(url, user, format="json")
        assert response.status_code == status.HTTP_400_BAD_REQUEST
