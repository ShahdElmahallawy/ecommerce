import pytest

from api.models.category import Category
from api.models.product import Product
from api.models.user import User
from api.models.order import Order
from api.models.payment import Payment

from api.selector.order import get_order_by_id_and_user, get_orders_by_user
from api.selector.category import get_all_categories, get_category_by_id, get_products_by_category

#categories
@pytest.mark.django_db
def test_get_all_categories():
    
    category1 = Category.objects.create(name='Category 1')
    category2 = Category.objects.create(name='Category 2')
    
    categories = get_all_categories()
    
    assert categories.count() == 2
    assert category1 in categories
    assert category2 in categories

@pytest.mark.django_db
def test_get_category_by_id():
    category = Category.objects.create(name='Category 1')
    
    result = get_category_by_id(category.pk)
    
    assert result is not None
    assert result.name == 'Category 1'

@pytest.mark.django_db
def test_get_category_by_id_non_existent():
    result = get_category_by_id(9999)
    
    assert result is None

@pytest.mark.django_db
def test_get_products_by_category():
    product1 = Product.objects.create(
        name='Product 1',
        price=10.00,
        description='Description for product 1',
        count=5,
        currency='USD'
    )
    product2 = Product.objects.create(
        name='Product 2',
        price=20.00,
        description='Description for product 2',
        count=10,
        currency='USD'
    )

    category = Category.objects.create(
        name='Category 1',
        featured_product=product1
    )
    
    category_products = Product.objects.filter(
        id__in=Category.objects.filter(featured_product=product1).values_list('featured_product', flat=True)
    )

    assert product1 in category_products
    assert product2 not in category_products


#order
@pytest.mark.django_db
def test_get_order_by_id_and_user():
    user = User.objects.create_user(
        password='password',
        email='testuser@example.com',
        name='Test User'
    )
    payment_method = Payment.objects.create(
        user=user,
        pan='1234567812345678',
        bank_name='Bank of Test',
        expiry_date='2025-12-31',
        cvv='123',
        card_type='credit'
    )

    order = Order.objects.create(
        user=user,
        payment_method=payment_method,
        status='pending',
        total_price=100.00
    )
    
    result = get_order_by_id_and_user(order.pk, user)
    
    assert result is not None
    assert result.pk == order.pk
    assert result.user == user
    assert result.payment_method == payment_method
    assert result.status == 'pending'
    assert result.total_price == 100.00


@pytest.mark.django_db
def test_get_order_by_id_and_user_non_existent():
    user = User.objects.create_user(name='testuser', password='password',email='testuser@example.com',)
    
    result = get_order_by_id_and_user(9999, user)
    
    assert result is None

@pytest.mark.django_db
def test_get_orders_by_user():
    user1 = User.objects.create_user(name='user1', password='password1',email='user1@example.com',)
    user2 = User.objects.create_user(name='user2', password='password2',email='user2@example.com',)
    payment_method1 = Payment.objects.create(user=user1,pan="123456789", card_type='credit')
    payment_method2 = Payment.objects.create(user=user2,pan="987654321", card_type='debit')

    order1 = Order.objects.create(
        user=user1,
        payment_method=payment_method1,
        status='completed',
        total_price=100.00
    )
    order2 = Order.objects.create(
        user=user1,
        payment_method=payment_method1,
        status='pending',
        total_price=150.00
    )
    order3 = Order.objects.create(
        user=user2,
        payment_method=payment_method2,
        status='shipped',
        total_price=200.00
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
    user = User.objects.create_user(name='testuser', password='password',email='testuser@example.com')
    
    orders = get_orders_by_user(user)
    
    assert orders.count() == 0
