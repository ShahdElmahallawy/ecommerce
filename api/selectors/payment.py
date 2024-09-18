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
    try:
        payment = Payment.objects.get(id=payment_id, user=user)
    except Payment.DoesNotExist:
        return None
    return payment


def get_payment_by_id(payment_id):

    payment = Payment.objects.get(id=payment_id)

    return payment
