from django.shortcuts import get_object_or_404
from api.models import Payment


def list_payments(user):
    """
    Get the payment with the given ID.

    Returns:
    The payment with the given ID.
    """
    return Payment.objects.filter(user=user)


def get_payment(payment_id, user):
    """
    Get the payment with the given ID.

    Returns:
    The payment with the given ID.
    """
    return get_object_or_404(Payment, id=payment_id, user=user)
