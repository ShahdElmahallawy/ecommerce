from api.models.discount import Discount
from django.utils import timezone


def get_discount_by_code(user, code):
    try:
        discount = Discount.objects.get(user=user, code=code, is_active=True)
    except Discount.DoesNotExist:
        return None
    return discount


def get_active_discounts(user):
    now = timezone.now()
    return Discount.objects.filter(
        user=user, is_active=True, start_date__lte=now, end_date__gte=now
    )


def get_discount_by_id(discount_id):

    try:
        return Discount.objects.get(id=discount_id)
    except Discount.DoesNotExist:
        return None
