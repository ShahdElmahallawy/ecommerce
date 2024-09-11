from django.db.models import Sum, Avg
from api.models import Product, OrderItem


def get_top_selling_products(limit=10):
    return (
        OrderItem.objects.select_related("product__created_by")
        .values("product__id", "product__created_by")
        .annotate(total_sales=Sum("quantity"))
        .order_by("-total_sales")[:limit]
    )


def get_top_rated_products(limit=10):
    return (
        Product.objects.select_related("created_by")
        .annotate(avg_rating=Avg("reviews__rating"))
        .order_by("-avg_rating")[:limit]
    )


def get_products_by_ids(product_ids):
    return Product.objects.filter(id__in=product_ids)
