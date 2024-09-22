from datetime import timedelta
import pytest
from django.utils import timezone
from api.models import Order, OrderItem
from api.tasks import process_settlements
from api.tests.factories import (
    UserFactory,
    PaymentFactory,
    ProductFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_process_settlements():

    user = UserFactory(user_type="seller")

    payment_method = PaymentFactory(user=user)

    product = ProductFactory(created_by=user)

    order = OrderFactory(
        user=user,
        payment_method=payment_method,
        status="delivered",
        total_price=200.00,
        settled=False,
    )

    sixteen_days_ago = timezone.now() - timedelta(days=16)
    Order.objects.filter(id=order.id).update(
        created_at=sixteen_days_ago, updated_at=sixteen_days_ago
    )

    OrderItemFactory(order=order, product=product, quantity=2, unit_price=100.00)

    process_settlements()

    order.refresh_from_db()
    assert order.settled is True
