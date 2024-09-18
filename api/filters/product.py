from django_filters.rest_framework import FilterSet

from api.models import Product


class ProductFilter(FilterSet):
    class Meta:
        model = Product
        fields = {
            "price": ["gt", "lt"],
            "category": ["exact"],
            "supplier": ["exact"],
            "created_at": ["gt", "lt"],
        }


class ProductRatingFilter(FilterSet):
    @staticmethod
    def filter_rating(queryset, queryset_params):
        rating_gt = queryset_params.get("rating__gt")
        rating_lt = queryset_params.get("rating__lt")
        rating = queryset_params.get("rating")

        if rating:
            queryset = queryset.filter(rating=rating)

        if rating_gt:
            queryset = queryset.filter(rating__gt=rating_gt)

        if rating_lt:
            queryset = queryset.filter(rating__lt=rating_lt)

        return queryset
