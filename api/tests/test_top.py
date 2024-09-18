import pytest
from django.urls import reverse
from rest_framework import status
from api.models.order_item import OrderItem
from api.models.product import Product
from api.models.review import Review


@pytest.fixture
def create_product(db, admin):
    def _create_product(name, price, seller=None):
        return Product.objects.create(
            name=name,
            price=price,
            count=100,
            created_by=seller or admin,
            description="Test product",
            currency="USD",
        )

    return _create_product


@pytest.fixture
def create_order_item(order, product):
    def _create_order_item(quantity):
        return OrderItem.objects.create(
            order=order, product=product, quantity=quantity, unit_price=product.price
        )

    return _create_order_item


@pytest.fixture
def create_review(db):
    def _create_review(product, rating, user):
        return Review.objects.create(product=product, rating=rating, user=user)

    return _create_review


@pytest.mark.django_db
def test_top_selling_products_all_sellers(
    api_client_auth, admin, user, create_product, create_order_item, order
):
    product1 = create_product("Product 1", 10.00, admin)
    product2 = create_product("Product 2", 20.00, admin)

    OrderItem.objects.create(
        order=order, product=product1, quantity=5, unit_price=product1.price
    )
    OrderItem.objects.create(
        order=order, product=product2, quantity=3, unit_price=product2.price
    )

    url = reverse("top-selling-products")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    print(len(response.data))
    assert len(response.data) == 2
    assert response.data[0]["name"] == "Product 1"


@pytest.mark.django_db
def test_top_selling_products_single_seller(
    api_client_auth, admin, create_product, create_order_item, order
):
    products = [create_product(f"Product {i}", 10.00 * i, admin) for i in range(1, 4)]
    for i, product in enumerate(products, start=1):
        OrderItem.objects.create(
            order=order, product=product, quantity=i, unit_price=product.price
        )

    url = reverse("top-selling-products")
    response = api_client_auth.get(f"{url}?seller_id={admin.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_top_rated_products_all_sellers(
    api_client_auth, admin, user, create_product, create_review
):
    product1 = create_product("Product 1", 10.00, admin)
    product2 = create_product("Product 2", 20.00, admin)
    product3 = create_product("Product 3", 30.00, admin)

    create_review(product1, 5, admin)
    create_review(product2, 3, admin)
    create_review(product3, 4, admin)

    url = reverse("top-rated-products")
    response = api_client_auth.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]["name"] == "Product 1"


@pytest.mark.django_db
def test_top_rated_products_single_seller(
    api_client_auth, admin, create_product, create_review, user
):
    products = [create_product(f"Product {i}", 10.00 * i, admin) for i in range(1, 4)]
    ratings = [5, 3, 4]
    for product, rating in zip(products, ratings):
        create_review(product, rating, user=user)

    url = reverse("top-rated-products")
    response = api_client_auth.get(f"{url}?seller_id={admin.id}")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
    assert response.data[0]["name"] == "Product 1"


@pytest.mark.django_db
def test_top_selling_products_with_limit(
    api_client_auth, admin, create_product, create_order_item, order
):
    products = [create_product(f"Product {i}", 10.00 * i, admin) for i in range(1, 6)]
    for i, product in enumerate(products, start=1):
        OrderItem.objects.create(
            order=order, product=product, quantity=i, unit_price=product.price
        )

    url = reverse("top-selling-products")
    response = api_client_auth.get(f"{url}?limit=3")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3


@pytest.mark.django_db
def test_top_rated_products_with_limit(
    api_client_auth, admin, create_product, create_review, user
):
    products = [create_product(f"Product {i}", 10.00 * i, admin) for i in range(1, 6)]
    for i, product in enumerate(products, start=1):
        create_review(product, 6 - i, user=user)

    url = reverse("top-rated-products")
    response = api_client_auth.get(f"{url}?limit=3")

    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == 3
