from api.services import create_payment, update_payment, delete_payment
from api.models.payment import Payment
import pytest


@pytest.mark.django_db
def test_create_payment(user):
    data = {
        "pan": "1234567890123456",
        "bank_name": "CIB",
        "expiry_date": "2024-12-12",
        "cvv": "123",
        "card_type": "credit",
    }

    payment = create_payment(data, user)

    assert payment.pan == data["pan"]
    assert payment.bank_name == data["bank_name"]
    assert payment.user == user


@pytest.mark.django_db
def test_update_payment(user, payment):

    updated_data = {"bank_name": "HSBC"}

    updated_payment = update_payment(updated_data, payment)

    assert updated_payment.bank_name == "HSBC"
    assert updated_payment.pan == "1234567890123456"


@pytest.mark.django_db
def test_delete_payment(user, payment):

    delete_payment(payment)

    assert Payment.objects.filter(id=payment.id).exists() == False
