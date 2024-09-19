from django.utils.timezone import now, timedelta
from api.models import OrderItem


def get_daily_sales_for_seller(seller):
    start_time = now().replace(hour=0, minute=0, second=0, microsecond=0)
    return OrderItem.objects.filter(
        product__created_by=seller, order__created_at__gte=start_time
    )


def get_weekly_sales_for_seller(seller):
    start_time = now() - timedelta(days=now().weekday())
    return OrderItem.objects.filter(
        product__created_by=seller, order__created_at__gte=start_time
    )


def get_monthly_sales_for_seller(seller):
    start_time = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return OrderItem.objects.filter(
        product__created_by=seller, order__created_at__gte=start_time
    )
