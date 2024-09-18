import pytest
from api.models import Product, Review
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def user_data():
    return {
        "email": "user@example.com",
        "name": "User Test",
    }


@pytest.fixture
def product(db):
    return Product.objects.create(name="Product", price=10, count=10)


@pytest.mark.django_db
def test_get_reviews_by_product_view(product, user, api_client_auth):
    url = reverse("product-reviews", args=[product.id])
    response = api_client_auth.get(url)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_create_review_view(product, user, api_client_auth):
    url = reverse("create-review", args=[product.id])
    data = {"rating": 4, "text": "Review"}

    response = api_client_auth.post(url, data)
    assert response.status_code == 201


def test_create_review_view_fail(product, user, api_client_auth):
    # invalid rating
    url = reverse("create-review", args=[product.id])
    data = {"rating": -4, "text": "Review"}
    response = api_client_auth.post(url, data)
    assert response.status_code == 400

    # invalid product id
    data = {"rating": 4, "text": "Review"}
    url = reverse("create-review", args=[product.id + 1])
    response = api_client_auth.post(url, data)
    assert response.status_code == 400

    # invalid text
    data = {"rating": 4, "text": "<script>alert('XSS')</script>"}
    url = reverse("create-review", args=[product.id])
    response = api_client_auth.post(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_update_review_view(product, user, api_client_auth):
    review = Review.objects.create(product=product, rating=5, text="Review", user=user)
    url = reverse("update-review", args=[review.id])
    data = {"rating": 4, "text": "Updated Review"}

    response = api_client_auth.patch(url, data)
    assert response.status_code == 200

    user2 = User.objects.create_user(email="user2@example.com", name="User2")
    api_client_auth.force_authenticate(user2)
    response = api_client_auth.patch(url, data)
    assert response.status_code == 400


@pytest.mark.django_db
def test_delete_review_view(product, user, api_client_auth):
    review = Review.objects.create(product=product, rating=5, text="Review", user=user)
    url = reverse("delete-review", args=[review.id])

    response = api_client_auth.delete(url)
    assert response.status_code == 200

    user2 = User.objects.create_user(email="user2@example.com", name="User2")
    api_client_auth.force_authenticate(user2)
    response = api_client_auth.delete(url)
    assert response.status_code == 400
