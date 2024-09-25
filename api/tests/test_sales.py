import pytest
from django.utils.timezone import now, timedelta
from api.selectors.sales import (
    get_daily_sales_for_seller,
    get_weekly_sales_for_seller,
    get_monthly_sales_for_seller,
)
from api.models import OrderItem
from api.tests.factories import OrderItemFactory
from api.services.sales import (
    get_daily_sales_stats,
    get_weekly_sales_stats,
    get_monthly_sales_stats,
)
from decimal import Decimal

from django.urls import reverse
from rest_framework import status


# test selectors
@pytest.mark.django_db
def test_get_daily_sales_for_seller_with_backdated_order(user, product):

    yesterday = now() - timedelta(days=1)
    order_item_today = OrderItemFactory(product=product, order__created_at=yesterday)

    result = get_daily_sales_for_seller(product.created_by)

    assert result.count() == 1
    assert result.first() == order_item_today


@pytest.mark.django_db
def test_get_weekly_sales_for_seller_with_backdated_order(user, product):
    last_week = now() - timedelta(days=7)
    order_item_this_week = OrderItemFactory(
        product=product, order__created_at=last_week
    )

    result = get_weekly_sales_for_seller(product.created_by)

    assert result.count() == 1
    assert result.first() == order_item_this_week


@pytest.mark.django_db
def test_get_monthly_sales_for_seller_with_backdated_order(user, product):
    last_month = now() - timedelta(days=30)
    order_item_this_month = OrderItemFactory(
        product=product, order__created_at=last_month
    )

    result = get_monthly_sales_for_seller(product.created_by)

    assert result.count() == 1
    assert result.first() == order_item_this_month


# test services


@pytest.mark.django_db
def test_get_daily_sales_stats_with_backdated_order(user, product):

    yesterday = now() - timedelta(days=1)
    OrderItemFactory(
        product=product,
        quantity=2,
        unit_price=Decimal("50.00"),
        order__created_at=yesterday,
    )

    result = get_daily_sales_stats(user)

    assert result["total_sales_amount"] == 2
    assert result["total_orders_count"] == 1


@pytest.mark.django_db
def test_get_weekly_sales_stats_with_backdated_order(user, product):

    last_week = now() - timedelta(days=7)
    OrderItemFactory(
        product=product,
        quantity=2,
        unit_price=Decimal("60.00"),
        order__created_at=last_week,
    )

    result = get_weekly_sales_stats(user)

    assert result["total_sales_amount"] == 2
    assert result["total_orders_count"] == 1


@pytest.mark.django_db
def test_get_monthly_sales_stats_with_backdated_order(user, product):

    last_month = now() - timedelta(days=30)
    OrderItemFactory(
        product=product,
        quantity=5,
        unit_price=Decimal("70.00"),
        order__created_at=last_month,
    )

    result = get_monthly_sales_stats(user)

    assert result["total_sales_amount"] == 5
    assert result["total_orders_count"] == 1


# test views


@pytest.mark.django_db
def test_daily_sales_view_with_backdated_order(api_client_auth, user, product):

    yesterday = now() - timedelta(days=1)
    OrderItemFactory(
        product=product,
        order__created_at=yesterday,
        quantity=1,
        unit_price=Decimal("20.00"),
    )

    url = reverse("daily-sales")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_sales_amount"] == 1
    assert data["total_orders_count"] == 1


@pytest.mark.django_db
def test_weekly_sales_view_with_backdated_order(api_client_auth, user, product):

    last_week = now() - timedelta(days=7)
    OrderItemFactory(
        product=product,
        order__created_at=last_week,
        quantity=1,
        unit_price=Decimal("40.00"),
    )

    url = reverse("weekly-sales")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_sales_amount"] == 1
    assert data["total_orders_count"] == 1


# tested two orders
@pytest.mark.django_db
def test_monthly_sales_view_with_backdated_order(api_client_auth, user, product):

    OrderItemFactory(product=product, quantity=5, unit_price=Decimal("70.00"))

    last_month = now() - timedelta(days=30)
    OrderItemFactory(
        product=product,
        order__created_at=last_month,
        quantity=1,
        unit_price=Decimal("50.00"),
    )

    url = reverse("monthly-sales")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["total_sales_amount"] == 6
    assert data["total_orders_count"] == 2
