import pytest
from django.urls import reverse
from rest_framework import status
from api.models.product import Product
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.payment import Payment

from api.services.order import create_order


@pytest.fixture
def user_data():
    return {
        "email": "amr@example.com",
        "name": "Amr Test",
    }


@pytest.fixture
def payment(user):
    return Payment.objects.create(
        user=user,
        pan="1234567890123456",
        bank_name="CIB",
        expiry_date="2024-12-12",
        cvv="123",
        card_type="credit",
    )


@pytest.mark.django_db
def test_create_order_success(api_client_auth, payment):

    product1 = Product.objects.create(name="Product 1", price=100.00, count=5)
    product2 = Product.objects.create(name="Product 2", price=200.00, count=3)

    url = reverse("orders:create")

    data = {
        "payment_method": payment.id,
        "items": [
            {"product_id": product1.id, "quantity": 2},
            {"product_id": product2.id, "quantity": 1},
        ],
    }

    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == status.HTTP_201_CREATED
    assert response.data["user"] == payment.user.id
    assert response.data["status"] == "pending"
    assert len(response.data["items"]) == 2

    assert Order.objects.count() == 1
    assert Order.objects.get().user == payment.user
    assert Order.objects.get().status == "pending"
    assert OrderItem.objects.count() == 2

    product1.refresh_from_db()
    product2.refresh_from_db()

    assert product1.count == 3
    assert product2.count == 2


@pytest.mark.django_db
def test_create_order_failure(api_client_auth, payment):
    url = reverse("orders:create")

    data = {
        "payment_method": payment.id,
        "items": [
            {"product_id": 99999, "quantity": 2},
        ],
    }

    response = api_client_auth.post(url, data, format="json")
    assert "error" in response.data


@pytest.mark.django_db
def test_order_deliver_success(api_admin_auth, admin, payment):
    product = Product.objects.create(name="Product", price=100.00, count=5)

    order = create_order(admin, payment, [{"product_id": product.id, "quantity": 1}])

    assert order is not None
    assert order.items.count() == 1
    assert order.total_price == 100.00
