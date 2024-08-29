import pytest

from api.models import Payment


@pytest.mark.django_db
def test_save_method_sets_default_payment(user):
    """Test that the save method sets the default payment."""
    payment1 = Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
        default=False,
    )
    payment1.refresh_from_db()
    assert payment1.default == True
    assert Payment.objects.filter(user=user, default=True).count() == 1

    payment2 = Payment.objects.create(
        user=user,
        pan="1234567890123457",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
        default=True,
    )

    payment1.refresh_from_db()
    assert payment1.default == False
    assert Payment.objects.filter(user=user, default=True).count() == 1


@pytest.mark.django_db
def test_delete_method_does_not_delete_default_payment(user):
    """Test that the delete method does not delete the default payment."""
    payment = Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
        default=True,
    )
    assert Payment.objects.filter(user=user, default=True).count() == 1
    with pytest.raises(Exception):
        payment.delete()
