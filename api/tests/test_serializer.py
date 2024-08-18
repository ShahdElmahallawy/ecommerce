import pytest
from api.serializers.category import CategorySerializer
from api.serializers.order import OrderSerializer
from api.models.category import Category
from api.models.order import Order
from api.models.order_item import OrderItem
from api.models.product import Product
from api.models.user import User
from api.models.payment import Payment

@pytest.mark.django_db
def test_category_serializer():
    product = Product.objects.create(name="Test Product", price=10.00, count=10)
    category = Category.objects.create(name="Test Category", featred_product=product)
    serializer = CategorySerializer(category)
    data = serializer.data
    
    assert data['name'] == category.name
    assert data['featred_product'] == product.id  


@pytest.mark.django_db
def test_order_serializer():
    user = User.objects.create(email="testuser@example.com", name="Test User", password="password")
    
    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit"
    )
    
    order = Order.objects.create(user=user, payment_method=payment)
    
    product = Product.objects.create(name="Test Product", price=10.00, count=10)
    order_item = OrderItem.objects.create(order=order, product=product, quantity=2, unit_price=10.00)
    
    serializer = OrderSerializer(order)
    data = serializer.data
    
    assert data['user'] == user.id
    assert data['payment_method'] == payment.id
    assert len(data['items']) == 1
    assert data['items'][0]['product'] == product.id
    assert data['items'][0]['quantity'] == order_item.quantity
    
    assert float(data['items'][0]['unit_price']) == float(order_item.unit_price)