import pytest
from api.selectors.product import list_products
from api.filters.product import ProductRatingFilter
from api.tests.factories import ProductFactory, ReviewFactory, UserFactory


@pytest.fixture
def products_with_reviews():
    product1 = ProductFactory(image=None, created_by=None, supplier=None)
    product2 = ProductFactory(image=None, created_by=None, supplier=None)
    product3 = ProductFactory(image=None, created_by=None, supplier=None)
    user = UserFactory(password=None)
    ReviewFactory(product=product1, rating=2, user=user)
    ReviewFactory(product=product2, rating=4, user=user)
    ReviewFactory(product=product3, rating=3, user=user)
    return product1, product2, product3


@pytest.mark.django_db
def test_filter_rating(products_with_reviews):
    product1, product2, product3 = products_with_reviews

    # filter by rating equal to
    queryset_params = {"rating": 2}
    queryset = list_products()
    filtered_queryset = ProductRatingFilter.filter_rating(queryset, queryset_params)
    assert filtered_queryset.count() == 1
    assert product1 in filtered_queryset

    # filter by rating greater than
    queryset_params = {"rating__gt": 2}
    filtered_queryset = ProductRatingFilter.filter_rating(queryset, queryset_params)
    assert filtered_queryset.count() == 2
    assert product2 in filtered_queryset
    assert product3 in filtered_queryset

    # filter by rating less than
    queryset_params = {"rating__lt": 3}
    filtered_queryset = ProductRatingFilter.filter_rating(queryset, queryset_params)
    assert filtered_queryset.count() == 1
    assert product1 in filtered_queryset

    # filter by rating between
    queryset_params = {"rating__gt": 2, "rating__lt": 4.5}
    filtered_queryset = ProductRatingFilter.filter_rating(queryset, queryset_params)
    assert filtered_queryset.count() == 2
    assert product3 in filtered_queryset
    assert product2 in filtered_queryset

    # no filter
    queryset_params = {}
    filtered_queryset = ProductRatingFilter.filter_rating(queryset, queryset_params)
    assert filtered_queryset.count() == 3
    assert product1 in filtered_queryset
    assert product2 in filtered_queryset
    assert product3 in filtered_queryset
