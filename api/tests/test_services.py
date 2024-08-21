import pytest
from api.service.category import update_category, delete_category
from api.models.category import Category

import pytest
from api.service.order import cancel_order
from api.models.order import Order
from api.models.user import User
from api.models.payment import Payment 

@pytest.mark.django_db
def test_update_category():
    category = Category.objects.create(name="Old Name")
    category_id = category.id

    update_data = {
        "name": "New Name"
    }

    updated_category = update_category(category_id, update_data)

    category = Category.objects.get(pk=category_id)

    assert updated_category is not None
    assert updated_category.id == category_id
    assert category.name == "New Name"

@pytest.mark.django_db
def test_delete_category():
    category = Category.objects.create(name="Category to Delete")
    category_id = category.id

    delete_category(category_id)

    category = Category.objects.filter(pk=category_id).first()

    assert category is None


@pytest.mark.django_db
def test_cancel_order_success():
    user = User.objects.create_user(name="testuser", password="password123", email="testuser@example.com")

    payment_method = Payment.objects.create(user=user,card_type="debit")  

    order = Order.objects.create(
        status="pending",
        user=user,
        payment_method=payment_method,
    )
    order_id = order.id

    response, success = cancel_order(order_id, user)

    updated_order = Order.objects.get(pk=order_id)

    assert success is True
    assert response == {"status": "Order cancelled"}
    assert updated_order.status == "cancelled"


@pytest.mark.django_db
def test_cancel_order_not_found():
    user = User.objects.create_user(name="testuser", password="password123",  email="testuser@example.com")

    non_existent_order_id = 9999

    response, success = cancel_order(non_existent_order_id, user)

    assert success is False
    assert response == {"error": "Order not found"}

@pytest.mark.django_db
def test_cancel_order_not_pending():
    user = User.objects.create_user(name="testuser", password="password123", email="testuser@example.com")

    payment_method = Payment.objects.create(user=user,card_type="debit")  


    order = Order.objects.create(
        status="completed",
        user=user,
        payment_method = payment_method

    )
    order_id = order.id

    response, success = cancel_order(order_id, user)

    assert success is False
    assert response == {"error": "Order cannot be cancelled"}


