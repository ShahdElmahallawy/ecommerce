import pytest

from django.contrib.auth import get_user_model


@pytest.mark.django_db
def test_create_user_successful():
    email = "amr@example.com"
    name = "Amr Test"
    password = "test1234"
    user = get_user_model().objects.create_user(
        email=email, name=name, password=password
    )

    assert email == user.email
    assert name == user.name
    assert user.check_password(password)


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError):
        get_user_model().objects.create_user(
            email="", name="amr test", password="test1234"
        )


@pytest.mark.django_db
def test_create_user_normalize_email():
    emails = [
        ["test1@EXAMPLE.com", "test1@example.com"],
        ["Test2@Example.com", "Test2@example.com"],
        ["TEST3@EXAMPLE.com", "TEST3@example.com"],
        ["test4@example.COM", "test4@example.com"],
    ]
    for email, expected_email in emails:
        user = get_user_model().objects.create_user(
            email=email, name="amr test", password="test1234"
        )

        assert expected_email == user.email


@pytest.mark.django_db
def test_create_superuser():
    user = get_user_model().objects.create_superuser(
        email="amr@example.com", name="amr test", password="test1234"
    )

    assert user.is_superuser
    assert user.is_staff
