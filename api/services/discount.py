from api.selectors.discount import get_discount_by_code
from django.utils import timezone


def apply_discount_to_order(user, discount_code, total_price):

    discount = get_discount_by_code(user, discount_code)

    if not discount:
        return None, "Invalid or expired discount code."

    if not discount.is_active or not discount.is_valid:
        return None, "This discount is no longer valid."

    discount_amount = total_price * (discount.discount_percentage / 100)
    discounted_price = total_price - discount_amount

    return discounted_price, None
