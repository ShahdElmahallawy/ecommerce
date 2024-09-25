from api.models.payment import Payment
import pytest
from django.urls import reverse
from rest_framework import status


@pytest.mark.django_db
def test_payment_list(api_client_auth, payment):
    url = reverse("payment-list")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 1


@pytest.mark.django_db
def test_payment_detail(api_client_auth, payment):
    url = reverse("payment-detail", kwargs={"payment_id": payment.id})
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pan"] == payment.pan


@pytest.mark.django_db
def test_payment_detail_not_found(api_client_auth, payment):
    url = reverse("payment-detail", kwargs={"payment_id": 2})
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_create_payment(api_client_auth, user):
    url = reverse("payment-create")
    data = {
        "pan": "1111222233334444",
        "bank_name": "HSBC",
        "expiry_date": "12/25",
        "cvv": "999",
        "card_type": "credit",
    }
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Payment.objects.filter(pan="1111222233334444").exists()


@pytest.mark.django_db
def test_create_payment_invalid(api_client_auth, user):
    url = reverse("payment-create")
    # invalid pan
    data = {
        "pan": "111122223333444",
        "bank_name": "HSBC",
        "expiry_date": "12/25",
        "cvv": "999",
        "card_type": "credit",
    }
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    # invalid cvv
    data["pan"] = "1111222233334444"
    data["cvv"] = "99"
    response = api_client_auth.post(url, data, format="json")
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_create_payment_invalid_expiry_date(api_client_auth, user):
    url = reverse("payment-create")
    data = {
        "pan": "1111222233334444",
        "bank_name": "HSBC",
        "expiry_date": "11/12/2025",
        "cvv": "999",
        "card_type": "credit",
    }
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_update_payment(api_client_auth, payment):
    url = reverse("payment-update", kwargs={"payment_id": payment.id})
    data = {"bank_name": "HSBC"}
    response = api_client_auth.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    payment.refresh_from_db()
    assert payment.bank_name == "HSBC"


@pytest.mark.django_db
def test_update_payment_not_found(api_client_auth, payment):
    url = reverse("payment-update", kwargs={"payment_id": 2})
    data = {"bank_name": "HSBC"}
    response = api_client_auth.patch(url, data, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_delete_payment(api_client_auth, payment):
    url = reverse("payment-delete", kwargs={"payment_id": payment.id})
    response = api_client_auth.delete(url, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_payment(api_client_auth, user, payment):
    payment2 = Payment.objects.create(
        user=user,
        pan="1234567890123457",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
        default=True,
    )

    url = reverse("payment-delete", kwargs={"payment_id": payment.id})
    response = api_client_auth.delete(url, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT


@pytest.mark.django_db
def test_delete_payment_fail(api_client_auth, user, payment):
    url = reverse("payment-delete", kwargs={"payment_id": payment.id})

    response = api_client_auth.delete(url, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_delete_payment_not_found(api_client_auth, payment):
    url = reverse("payment-delete", kwargs={"payment_id": 2})
    response = api_client_auth.delete(url, format="json")

    assert response.status_code == status.HTTP_404_NOT_FOUND
