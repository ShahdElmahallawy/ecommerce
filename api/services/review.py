from api.selectors.review import (
    get_review_for_edit,
)
from api.models import Review
from django.contrib.auth import get_user_model
from rest_framework.exceptions import ValidationError

User = get_user_model()


def create_review(user, product, rating, text):
    """
    Create a review for a product.
    """
    return Review.objects.create(user=user, product=product, rating=rating, text=text)


def update_review(review_id, user, data):
    """
    Update a review.
    """
    review = get_review_for_edit(user, review_id)
    if not review:
        raise ValidationError({"detail": "No available review found with the given ID."})
    for field, value in data.items():
        setattr(review, field, value)
    review.save(update_fields=["rating", "text"])
    return review


def delete_review(review_id, user):
    """
    Delete a review.
    """
    review = get_review_for_edit(user, review_id)
    if not review:
        raise ValidationError({"detail": "No available review found with the given ID."})
    review.delete()
    return None
