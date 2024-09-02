from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.serializers.review import ReviewSerializer
from api.services.review import create_review, update_review, delete_review
from api.selectors.review import get_reviews_by_product
from rest_framework.permissions import IsAuthenticated


class GetReviewsByProductView(APIView):
    """
    View to get all reviews for a product.
    """

    def get(self, request, product_id):
        reviews = get_reviews_by_product(product_id)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateReviewView(APIView):
    """
    View to create a review.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, product_id):
        serializer = ReviewSerializer(
            data=request.data, context={"product_id": product_id}
        )
        serializer.is_valid(raise_exception=True)
        review = create_review(
            request.user,
            serializer.validated_data["product"],
            serializer.validated_data["rating"],
            serializer.validated_data["text"],
        )
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UpdateReviewView(APIView):
    """
    View to update a review.
    """

    permission_classes = [IsAuthenticated]

    def patch(self, request, review_id):
        serializer = ReviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        review = update_review(review_id, request.user, serializer.validated_data)
        serializer = ReviewSerializer(review)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteReviewView(APIView):
    """
    View to delete a review.
    """

    permission_classes = [IsAuthenticated]

    def delete(self, request, review_id):
        delete_review(review_id, request.user)
        return Response(status=status.HTTP_200_OK)
