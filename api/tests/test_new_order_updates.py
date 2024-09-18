import pytest
from django.urls import reverse
from api.models.cart import Cart
from api.models.cart_item import CartItem
from api.models.order import Order

from api.models.order_item import OrderItem
from api.models.payment import Payment


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
def test_create_order_success(api_client_auth, user, product, payment):

    url = reverse("orders:create")
    data = {"payment_method": payment.id}

    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=2)

    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == 201
    response_data = response.json()
    assert "id" in response_data
    assert response_data["total_price"] == "200.00"
    assert len(response_data["items"]) == 1

    assert CartItem.objects.filter(cart=cart).count() == 0

    assert Order.objects.filter(user=user).count() == 1


@pytest.mark.django_db
def test_create_order_empty_cart(api_client_auth, user, payment):

    url = reverse("orders:create")
    data = {"payment_method": payment.id}
    cart = Cart.objects.create(user=user)
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == 400
    assert response.json()["detail"] == "The cart is empty"


@pytest.mark.django_db
def test_create_order_invalid_payment_method(api_client_auth, user, product):

    url = reverse("orders:create")

    invalid_payment_method_id = "haha"
    data = {"payment_method": invalid_payment_method_id}
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, product=product, quantity=2)
    response = api_client_auth.post(url, data, format="json")

    assert response.status_code == 400
