from smtplib import SMTPException
from unittest.mock import patch
from django.urls import reverse
import pytest
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError, APIException

from api.services import (
    create_user,
    get_tokens_for_user,
    get_refreshed_tokens,
    generate_reset_password_token,
    reset_user_password,
    generate_otp_for_user,
)


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


@pytest.mark.django_db
@patch("api.utils.mails.send_mail")
def test_generate_otp_for_user(mock_send_email, user):
    generate_otp_for_user(user)

    assert user.otp_code
    assert mock_send_email.called


@pytest.mark.django_db
@patch("api.utils.mails.send_mail")
def test_generate_otp_for_user_fail(mock_send_email, user):
    generate_otp_for_user(user)
    mock_send_email.side_effect = SMTPException("Email sending failed")

    with pytest.raises(APIException):
        generate_otp_for_user(user)


@pytest.mark.django_db
def test_get_tokens_for_user(user):
    tokens = get_tokens_for_user(user)

    assert "refresh" in tokens
    assert "access" in tokens


def test_get_refreshed_tokens(user):

    tokens = get_tokens_for_user(user)
    new_tokens = get_refreshed_tokens(tokens["refresh"])

    assert "refresh" in new_tokens
    assert "access" in new_tokens


def test_get_refreshed_tokens_fail():
    with pytest.raises(ValidationError):
        get_refreshed_tokens("invalid")


@pytest.mark.django_db
@patch("api.utils.mails.send_mail")
def test_generate_reset_password_token(mock_send_email, user, rf):
    mock_request = rf.get("/")
    generate_reset_password_token(user, mock_request)

    assert user.reset_password_token
    assert user.reset_password_token_expiry
    assert mock_send_email.called


@pytest.mark.django_db
@patch("api.utils.mails.send_mail")
def test_generate_reset_password_token_fail(mock_send_email, user, rf):
    mock_request = rf.get("/")
    mock_send_email.side_effect = Exception("Email sending failed")

    with pytest.raises(APIException):
        generate_reset_password_token(user, mock_request)


@patch("api.utils.mails.send_mail")
def test_generate_reset_password_token_fail(mock_send_email, user, rf):
    mock_request = rf.get("/")
    mock_send_email.side_effect = Exception("Email sending failed")
    with pytest.raises(APIException):
        generate_reset_password_token(user, mock_request)


def test_reset_user_password(user):
    new_password = "new_password12"
    reset_user_password(user, new_password)

    assert not user.reset_password_token
    assert not user.reset_password_token_expiry
    assert user.password_changed_at
