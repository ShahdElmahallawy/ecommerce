from django.db.models import Sum, Count
from api.selectors.sales import (
    get_daily_sales_for_seller,
    get_weekly_sales_for_seller,
    get_monthly_sales_for_seller,
)


def calculate_sales_data(order_items):
    total_sales_amount = (
        order_items.aggregate(total=Sum("quantity", field="quantity * unit_price"))[
            "total"
        ]
        or 0
    )

    total_orders_count = order_items.aggregate(
        order_count=Count("order", distinct=True)
    )["order_count"]

    return {
        "total_sales_amount": total_sales_amount,
        "total_orders_count": total_orders_count,
        "order_items": [
            {
                "order_id": item.order.id,
                "product": item.product.name,
                "quantity": item.quantity,
                "unit_price": item.unit_price,
                "total_price": item.quantity * item.unit_price,
                "order_date": item.order.created_at,
            }
            for item in order_items
        ],
    }


def get_daily_sales_stats(seller):
    order_items = get_daily_sales_for_seller(seller)
    return calculate_sales_data(order_items)


def get_weekly_sales_stats(seller):
    order_items = get_weekly_sales_for_seller(seller)
    return calculate_sales_data(order_items)


def get_monthly_sales_stats(seller):
    order_items = get_monthly_sales_for_seller(seller)
    return calculate_sales_data(order_items)
