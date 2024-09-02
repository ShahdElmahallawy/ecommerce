from api.models import Review


def get_reviews_by_product(product):
    """
    Get all reviews for the given product.
    """
    return Review.objects.filter(product=product)


def get_review_by_id(review_id):
    """
    Get a review by its ID.
    """
    try:
        return Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return None


def get_review_for_edit(user, review_id):
    """
    Get a review by its ID and user.
    """
    try:
        return Review.objects.get(id=review_id, user=user)
    except Review.DoesNotExist:
        return None
