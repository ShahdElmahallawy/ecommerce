import pytest
from api.models.category import Category
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.product import Product
from api.models.user import User
from api.models.payment import Payment


@pytest.mark.django_db
def test_category_creation():
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        name="Test Product", price=10.00, count=10, category=category
    )
    category.featured_product = product
    category.save()
    assert category.name == "Test Category"
    assert category.featured_product == product


@pytest.mark.django_db
def test_category_str():
    category = Category.objects.create(name="Test Category")
    assert str(category) == "Test Category"


@pytest.mark.django_db
def test_order_creation():

    user = User.objects.create(
        email="testuser@example.com", name="Test User", password="password"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, payment_method=payment)

    assert order.user == user
    assert order.status == "pending"
    assert order.payment_method == payment


@pytest.mark.django_db
def test_order_str():
    user = User.objects.create(
        email="testuser@example.com", name="Test User", password="password"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, payment_method=payment)

    assert str(order) == f"Order #{order.id}"


@pytest.mark.django_db
def test_order_total_price_calculation():
    user = User.objects.create(
        email="testuser@example.com", name="Test User", password="password"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, payment_method=payment)

    category = Category.objects.create(name="Test Category")
    product1 = Product.objects.create(
        name="Product 1", price=10.00, count=10, category=category
    )
    product2 = Product.objects.create(
        name="Product 2", price=20.00, count=10, category=category
    )

    OrderItem.objects.create(
        order=order, product=product1, quantity=2, unit_price=10.00
    )
    OrderItem.objects.create(
        order=order, product=product2, quantity=1, unit_price=20.00
    )

    order.calculate_total_price()

    assert order.total_price == 40.00


@pytest.mark.django_db
def test_order_item_creation():
    user = User.objects.create(
        email="testuser@example.com", name="Test User", password="password"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, payment_method=payment)
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        name="Test Product", price=10.00, count=10, category=category
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, quantity=2, unit_price=10.00
    )

    assert order_item.product == product
    assert order_item.quantity == 2
    assert order_item.unit_price == 10.00


@pytest.mark.django_db
def test_order_item_str():
    user = User.objects.create(
        email="testuser@example.com", name="Test User", password="password"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, payment_method=payment)
    category = Category.objects.create(name="Test Category")
    product = Product.objects.create(
        name="Test Product", price=10.00, count=10, category=category
    )

    order_item = OrderItem.objects.create(
        order=order, product=product, quantity=2, unit_price=10.00
    )

    assert str(order_item) == product.name
