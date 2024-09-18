import pytest
from api.selectors.order import get_order_by_id_and_user, get_orders_by_user
from api.selectors.category import (
    get_all_categories,
    get_category_by_id,
)
from api.tests.factories import (
    ProductFactory,
    UserFactory,
    OrderFactory,
    PaymentFactory,
    CategoryFactory,
)


# categories
@pytest.mark.django_db
def test_get_all_categories():
    category1 = CategoryFactory(name="Category 1")
    category2 = CategoryFactory(name="Category 2")

    categories = get_all_categories()

    assert categories.count() == 2
    assert category1 in categories
    assert category2 in categories


@pytest.mark.django_db
def test_get_category_by_id():
    category = CategoryFactory(name="Category 1")

    result = get_category_by_id(category.pk)

    assert result is not None
    assert result.name == "Category 1"


@pytest.mark.django_db
def test_get_category_by_id_non_existent():
    result = get_category_by_id(9999)

    assert result is None


@pytest.mark.django_db
def test_get_products_by_category():
    product1 = ProductFactory(name="Product 1")
    product2 = ProductFactory(name="Product 2")

    category = CategoryFactory(name="Category 1", featured_product=product1)

    category_products = ProductFactory._meta.model.objects.filter(
        id__in=category._meta.model.objects.filter(
            featured_product=product1
        ).values_list("featured_product", flat=True)
    )

    assert product1 in category_products
    assert product2 not in category_products


# order
@pytest.mark.django_db
def test_get_order_by_id_and_user():

    user = UserFactory(email="testuser@example.com", name="Test User", password=None)
    payment_method = PaymentFactory(
        user=user, pan="1234567812345678", bank_name="CIB", expiry_date="2024-12-12"
    )

    order = OrderFactory(
        user=user, payment_method=payment_method, status="pending", total_price=100.00
    )

    result = get_order_by_id_and_user(order.pk, user)

    assert result is not None
    assert result.pk == order.pk
    assert result.user == user
    assert result.payment_method == payment_method
    assert result.status == "pending"
    assert result.total_price == 100.00


@pytest.mark.django_db
def test_get_order_by_id_and_user_non_existent():

    user = UserFactory(email="testuser@example.com", name="Test User", password=None)

    result = get_order_by_id_and_user(9999, user)

    assert result is None


@pytest.mark.django_db
def test_get_orders_by_user():

    user1 = UserFactory(email="user1@example.com", name="User 1", password=None)
    user2 = UserFactory(email="user2@example.com", name="User 2", password=None)

    payment_method1 = PaymentFactory(
        user=user1, pan="123456789", expiry_date="2024-12-12"
    )
    payment_method2 = PaymentFactory(
        user=user2, pan="987654321", expiry_date="2024-12-12"
    )

    order1 = OrderFactory(
        user=user1,
        payment_method=payment_method1,
        status="completed",
        total_price=100.00,
    )
    order2 = OrderFactory(
        user=user1, payment_method=payment_method1, status="pending", total_price=150.00
    )
    order3 = OrderFactory(
        user=user2, payment_method=payment_method2, status="shipped", total_price=200.00
    )

    orders_user1 = get_orders_by_user(user1)
    orders_user2 = get_orders_by_user(user2)

    assert orders_user1.count() == 2
    assert order1 in orders_user1
    assert order2 in orders_user1

    assert orders_user2.count() == 1
    assert order3 in orders_user2


@pytest.mark.django_db
def test_get_orders_by_user_no_orders():

    user = UserFactory(email="testuser@example.com", name="Test User", password=None)

    orders = get_orders_by_user(user)

    assert orders.count() == 0
