import pytest
from api.selectors.review import (
    get_review_by_id,
    get_reviews_by_product,
    get_review_for_edit,
)
from api.models import Review
from api.tests.factories import ProductFactory, UserFactory
from api.tests.factories import ReviewFactory


@pytest.mark.django_db
def test_get_review_by_id():
    user = UserFactory()
    product = ProductFactory()

    review = ReviewFactory(product=product, user=user, rating=5, text="Review")

    assert get_review_by_id(review.id) == review


@pytest.mark.django_db
def test_get_reviews_by_product():
    user = UserFactory()
    product = ProductFactory()

    review = ReviewFactory(product=product, user=user, rating=5, text="Review")

    assert get_reviews_by_product(product).count() == 1

    product2 = ProductFactory(name="Product2")

    assert get_reviews_by_product(product2).count() == 0


@pytest.mark.django_db
def test_get_review_for_edit():
    user = UserFactory()
    user2 = UserFactory(email="user2@example.com", name="User2")
    product = ProductFactory()

    review = ReviewFactory(product=product, user=user, rating=5, text="Review")

    assert get_review_for_edit(user, review.id) == review

    assert get_review_for_edit(user, review.id + 1) is None

    assert get_review_for_edit(user2, review.id) is None
