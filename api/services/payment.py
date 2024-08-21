from api.models import Payment
from api.serializers.payment import PaymentSerializer


def create_payment(data, user):
    """
    Create a payment with the given data.

    Returns:
        The created payment.
    """
    payment = Payment.objects.create(**data, user=user)
    return payment


def update_payment(data, payment):
    """
    Update the given payment with the given data.

    Returns:
        The updated payment.
    """
    serializer = PaymentSerializer(payment, data=data, partial=True)
    serializer.is_valid(raise_exception=True)
    return serializer.save()


def delete_payment(payment):
    """
    Delete the given payment.

    Returns:
        None
    """
    payment.delete()
    return None
