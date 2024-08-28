import pytest
from rest_framework import status
from django.urls import reverse

from api.models.category import Category
from api.models.product import Product
from api.models.order import Order
from api.models.user import User
from api.models.payment import Payment

from api.serializers.category import CategorySerializer
from api.serializers.category_detail import CategoryDetailSerializer
from api.serializers.product_serializer import ProductSerializer
from api.serializers.order import OrderSerializer

from api.services.order import cancel_order


@pytest.mark.django_db
def test_category_list_view(api_client_auth):
    Category.objects.create(name="Category 1")
    Category.objects.create(name="Category 2")

    response = api_client_auth.get(reverse("categories:list"))

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 2
    assert set(item["name"] for item in response.data) == {"Category 1", "Category 2"}


@pytest.mark.django_db
def test_category_detail_view(api_client_auth):
    category = Category.objects.create(name="Category Detail")

    response = api_client_auth.get(
        reverse("categories:detail", kwargs={"pk": category.id})
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "Category Detail"


@pytest.mark.django_db
def test_category_update_view(api_admin_auth):
    category = Category.objects.create(
        name="Old Name",
    )

    update_data = {
        "name": "New Name",
    }

    response = api_admin_auth.put(
        reverse("categories:update", kwargs={"pk": category.id}),
        update_data,
        format="json",
    )

    updated_category = Category.objects.get(pk=category.id)

    assert response.status_code == status.HTTP_200_OK
    assert response.data["name"] == "New Name"
    assert updated_category.name == "New Name"


@pytest.mark.django_db
def test_category_delete_view(api_admin_auth):
    category = Category.objects.create(
        name="Category to Delete",
    )

    response = api_admin_auth.delete(
        reverse("categories:delete", kwargs={"pk": category.id})
    )

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert not Category.objects.filter(pk=category.id).exists()


@pytest.mark.django_db
def test_category_product_list_view(api_client_auth):
    category = Category.objects.create(name="Electronics")

    featured_product = Product.objects.create(
        name="Laptop",
        price=999.99,
        description="A high-performance laptop.",
        count=10,
        currency="USD",
    )
    category.featured_product = featured_product
    category.save()

    url = reverse("categories:products", args=[category.id])

    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    expected_data = {
        "id": featured_product.id,
        "name": "Laptop",
        "price": "999.99",
        "description": "A high-performance laptop.",
        "count": 10,
        "currency": "USD",
    }

    assert response.data[0]["id"] == expected_data["id"]
    assert response.data[0]["name"] == expected_data["name"]
    assert response.data[0]["price"] == expected_data["price"]
    assert response.data[0]["description"] == expected_data["description"]
    assert response.data[0]["count"] == expected_data["count"]
    assert response.data[0]["currency"] == expected_data["currency"]


@pytest.mark.django_db
def test_category_product_list(api_client_auth):

    product1 = Product.objects.create(
        name="Smartphone",
        price=699.99,
        description="A high-end smartphone",
        count=50,
        currency="USD",
    )

    category = Category.objects.create(name="Electronics", featured_product=product1)
    url = reverse("categories:products", kwargs={"category_pk": category.pk})

    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) > 0

    product_names = [product["name"] for product in response.data]
    assert "Smartphone" in product_names

    assert any(product["price"] == "699.99" for product in response.data)


# order views
@pytest.mark.django_db
def test_order_cancel_success(api_client_auth):
    user = User.objects.create_user(
        name="testuser", password="testpass", email="testuser@example.com"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, status="pending", payment_method=payment)

    api_client_auth.force_authenticate(user=user)

    url = reverse("orders:cancel", args=[order.id])

    response = api_client_auth.post(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data["status"] == "Order cancelled"
    assert Order.objects.get(id=order.id).status == "cancelled"


@pytest.mark.django_db
def test_order_cancel_failure(api_client_auth):
    user = User.objects.create_user(
        name="testuser", password="testpass", email="testuser@example.com"
    )
    another_user = User.objects.create_user(
        name="anotheruser", password="notcorrect", email="anotheruser@example.com"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, status="pending", payment_method=payment)

    api_client_auth.force_authenticate(user=another_user)

    url = reverse("orders:cancel", args=[order.id])

    response = api_client_auth.post(url)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "error" in response.data


@pytest.mark.django_db
def test_order_track(api_client_auth):
    user = User.objects.create_user(
        name="testuser", password="testpass", email="testuser@example.com"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, status="pending", payment_method=payment)

    api_client_auth.force_authenticate(user=user)

    url = reverse("orders:track", args=[order.id])

    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    serializer = OrderSerializer(order)
    assert response.data == serializer.data


@pytest.mark.django_db
def test_order_track_unauthorized(api_client_auth):
    user = User.objects.create_user(
        name="testuser", password="testpass", email="testuser@example.com"
    )
    another_user = User.objects.create_user(
        name="anotheruser", password="anotherpass", email="anotheruser@example.com"
    )

    payment = Payment.objects.create(
        user=user,
        pan="1234567812345678",
        bank_name="Test Bank",
        expiry_date="2030-12-31",
        cvv="123",
        card_type="credit",
    )

    order = Order.objects.create(user=user, status="pending", payment_method=payment)

    api_client_auth.force_authenticate(user=another_user)

    url = reverse("orders:track", args=[order.id])

    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.django_db
def test_order_list_no_orders(api_client_auth):
    user = User.objects.create_user(
        name="testuser", password="testpass", email="testuser@example.com"
    )

    api_client_auth.force_authenticate(user=user)

    url = reverse("orders:list")

    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK

    assert response.data == []
