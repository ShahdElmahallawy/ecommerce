from api.selectors import list_payments, get_payment
from django.contrib.auth import get_user_model
from api.models.payment import Payment

import pytest


@pytest.mark.django_db
def test_list_payments(user):
    user_2 = get_user_model().objects.create_user(
        email="user2@example.com", name="user2"
    )
    Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )
    Payment.objects.create(
        user=user,
        pan="1111222233334444",
        bank_name="HSBC",
        expiry_date="2025-11-11",
        cvv="321",
        card_type="debit",
    )
    Payment.objects.create(
        user=user_2,
        pan="5555666677778888",
        bank_name="Bank of America",
        expiry_date="2026-10-10",
        cvv="456",
        card_type="credit",
    )

    payments = list_payments(user)

    assert len(payments) == 2
    assert payments[0].pan == "1234567890123456"
    assert payments[1].pan == "1111222233334444"


@pytest.mark.django_db
def test_get_payment(user, payment):

    retrieved_payment = get_payment(payment.id, user)

    assert retrieved_payment == payment
    assert retrieved_payment.pan == "1234567890123456"


@pytest.mark.django_db
def test_get_payment_not_found(user, payment):

    retrieved_payment = get_payment(2, user)

    assert retrieved_payment == None
