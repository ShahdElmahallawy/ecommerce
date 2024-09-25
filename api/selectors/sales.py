from django.utils.timezone import now, timedelta
from api.models import OrderItem
from django.utils import timezone


def get_daily_sales_for_seller(seller):
    start_time = now().replace(hour=0, minute=0, second=0, microsecond=0)
    return OrderItem.objects.filter(
        product__created_by=seller, order__created_at__gte=start_time
    )


def get_weekly_sales_for_seller(seller):
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)
    return OrderItem.objects.filter(
        product__created_by=seller,
        order__created_at__gte=start_date,
        order__created_at__lte=end_date,
    )


def get_monthly_sales_for_seller(seller):
    start_time = now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return OrderItem.objects.filter(
        product__created_by=seller, order__created_at__gte=start_time
    )
