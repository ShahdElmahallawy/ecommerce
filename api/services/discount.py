from api.selectors.discount import get_discount_by_code
from django.utils import timezone

from api.models.discount import Discount


def apply_discount_to_order(discount_code, total_price):

    discount = get_discount_by_code(discount_code)
    print(discount)
    if not discount:
        return None, "Invalid or expired discount code."

    if not discount.is_active:
        return None, "This discount is no longer valid."

    discount_amount = total_price * (discount.discount_percentage / 100)
    discounted_price = total_price - discount_amount

    return discounted_price, None


def create_discount(validated_data):
    discount = Discount.objects.create(**validated_data)
    return discount
