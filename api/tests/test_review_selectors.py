import pytest
from api.selectors.review import (
    get_review_by_id,
    get_reviews_by_product,
    get_review_for_edit,
)
from api.models import Review, Product
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def product(db):
    return Product.objects.create(name="Product", price=10)


@pytest.mark.django_db
def test_get_review_by_id(product, user):
    review = Review.objects.create(product=product, rating=5, text="Review", user=user)
    assert get_review_by_id(review.id) == review

    assert get_review_by_id(review.id + 1) == None


@pytest.mark.django_db
def test_get_reviews_by_product(product, user):
    Review.objects.create(product=product, rating=5, text="Review", user=user)
    assert get_reviews_by_product(product).count() == 1

    product2 = Product.objects.create(name="Product2", price=10)
    assert get_reviews_by_product(product2).count() == 0


@pytest.mark.django_db
def test_get_review_for_edit(product, user):
    review = Review.objects.create(product=product, rating=5, text="Review", user=user)
    assert get_review_for_edit(user, review.id) == review
    assert get_review_for_edit(user, review.id + 1) == None

    user2 = User.objects.create_user(email="user2@example.com", name="User2")
    assert get_review_for_edit(user2, review.id) == None
