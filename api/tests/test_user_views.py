import os
import pytest
import hashlib
from datetime import timedelta

from unittest.mock import patch
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth import get_user_model

from rest_framework import status

from api.models import Profile
from api.services.user import get_tokens_for_user


User = get_user_model()


@pytest.mark.django_db
def test_user_register(api_client):
    url = reverse("user-register")

    user_data = {
        "email": "amr@example.com",
        "password": "test12345",
        "confirm_password": "test12345",
        "name": "Amr Test",
    }

    response = api_client.post(url, user_data, format="json")
    user_model = get_user_model()
    user = user_model.objects.get(email=user_data["email"])
    profile = Profile.objects.get(user=user)

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


@pytest.mark.django_db
def test_user_login(api_client, user):
    url = reverse("user-login")

    data = {
        "email": "amr@example.com",
        "password": "testpassword123",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "refresh" in response.data
    assert "access" in response.data


@pytest.mark.django_db
def test_refresh_token(api_client, user):
    tokens = get_tokens_for_user(user)
    url = reverse("refresh-token")

    data = {
        "refresh": tokens["refresh"],
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert "access" in response.data
    assert "refresh" in response.data


@pytest.mark.django_db
def test_refresh_token_fail(api_client, user):
    url = reverse("refresh-token")

    data = {
        "refresh": "testrefresh123",
    }

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@patch("api.utils.mails.send_mail")
@pytest.mark.django_db
def test_forgot_password(mock_send_mail, api_client, user):
    url = reverse("forgot-password")
    data = {"email": user.email}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.reset_password_token is not None
    assert user.reset_password_token_expiry > timezone.now()


@patch("api.utils.mails.send_mail")
@pytest.mark.django_db
def test_forgot_password_not_found_email(mock_send_mail, api_client, user):
    url = reverse("forgot-password")
    data = {"email": "unkown@example.cpm"}

    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    assert not mock_send_mail.called
    assert user.reset_password_token is None
    assert user.reset_password_token_expiry is None


@pytest.mark.django_db
def test_password_reset_valid_token(api_client, user):
    reset_token = os.urandom(32).hex()
    hashed_token = hashlib.sha256(reset_token.encode()).hexdigest()
    user.reset_password_token = hashed_token
    user.reset_password_token_expiry = timezone.now() + timedelta(minutes=15)
    user.save()

    url = reverse("password-reset", args=[reset_token])
    data = {"new_password": "newpassword123", "confirm_new_password": "newpassword123"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password("newpassword123")


@pytest.mark.django_db
def test_password_reset_invalid_token(api_client, user):
    url = reverse("password-reset", args=["invalidtoken"])
    data = {"new_password": "newpassword123", "confirm_new_password": "newpassword123"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["detail"] == "Invalid or expired token."


@pytest.mark.django_db
def test_password_reset_mismatched_passwords(api_client, user):
    reset_token = os.urandom(32).hex()
    hashed_token = hashlib.sha256(reset_token.encode()).hexdigest()
    user.reset_password_token = hashed_token
    user.reset_password_token_expiry = timezone.now() + timedelta(minutes=15)
    user.save()

    url = reverse("password-reset", args=[reset_token])
    data = {"new_password": "newpassword123", "confirm_new_password": "newpassword12"}
    response = api_client.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data["non_field_errors"][0] == "Passwords do not match."
