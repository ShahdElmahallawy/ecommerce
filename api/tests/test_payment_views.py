from api.models import Payment
import pytest
from django.urls import reverse
from rest_framework import status
from django.utils import timezone


@pytest.mark.django_db
def test_payment_list(api_client_auth, user):
    Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date=timezone.now().date(),
        cvv="123",
        card_type="credit",
    )
    Payment.objects.create(
        user=user,
        pan="6543210987654321",
        bank_name="HSBC",
        expiry_date="2024-12-12",
        cvv="321",
        card_type="debit",
    )

    url = reverse("payment-list")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2


@pytest.mark.django_db
def test_payment_detail(api_client_auth, user):
    payment = Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )

    url = reverse("payment-detail", kwargs={"payment_id": payment.id})
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["pan"] == payment.pan


@pytest.mark.django_db
def test_create_payment(api_client_auth, user):
    url = reverse("payment-list")
    data = {
        "pan": "1111222233334444",
        "bank_name": "HSBC",
        "expiry_date": "2024-12-12",
        "cvv": "999",
        "card_type": "credit",
    }
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert Payment.objects.filter(pan="1111222233334444").exists()


@pytest.mark.django_db
def test_update_payment(api_client_auth, user):
    payment = Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )

    url = reverse("payment-detail", kwargs={"payment_id": payment.id})
    data = {"bank_name": "HSBC"}
    response = api_client_auth.patch(url, data, format="json")

    assert response.status_code == status.HTTP_200_OK
    payment.refresh_from_db()
    assert payment.bank_name == "HSBC"


@pytest.mark.django_db
def test_delete_payment(api_client_auth, user):
    # Setup: Create a Payment instance
    payment = Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )

    url = reverse("payment-detail", kwargs={"payment_id": payment.id})
    response = api_client_auth.delete(url, format="json")

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Payment.objects.filter(id=payment.id).exists()
