import pytest

from api.services.review import (
    create_review,
    update_review,
    delete_review,
)
from api.models import Review, Product

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
def test_create_review(product, user):
    review = create_review(user, product, 5, "Review")
    assert review is not None
    assert review.product == product
    assert review.user == user
    assert review.rating == 5
    assert review.text == "Review"


@pytest.mark.django_db
def test_create_review_duplicate(product, user):
    create_review(user, product, 5, "Review")
    with pytest.raises(Exception):
        create_review(user, product, 5, "Review")


@pytest.mark.django_db
def test_update_review(product, user):
    review = create_review(user, product, 5, "Review")
    review = update_review(review.id, user, {"rating": 4, "text": "Updated Review"})
    assert review.rating == 4
    assert review.text == "Updated Review"

    user2 = User.objects.create_user(
        email="user2@example.com", password="password", name="User2"
    )
    with pytest.raises(Exception):
        update_review(review.id, user2, {"rating": 4, "text": "Updated Review"})


@pytest.mark.django_db
def test_delete_review(product, user):
    review = create_review(user, product, 5, "Review")
    delete_review(review.id, user)
    assert Review.objects.count() == 0

    review = create_review(user, product, 5, "Review")
    user2 = User.objects.create_user(email="user2@example.com", name="User2")
    with pytest.raises(Exception):
        delete_review(review.id, user2)
