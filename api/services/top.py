from django.db.models import Sum, Avg
from api.models import Product, OrderItem
from api.selectors.top import (
    get_top_selling_products,
    get_top_rated_products,
    get_products_by_ids,
)
from api.serializers import ProductSerializer


def group_products_by_seller(products, product_key, limit):
    sellers = {}
    for product in products:
        seller_id = (
            product["product__created_by"]
            if product_key == "top_selling"
            else product.created_by.id
        )
        product_id = (
            product["product__id"] if product_key == "top_selling" else product.id
        )

        if seller_id not in sellers:
            sellers[seller_id] = []
        if len(sellers[seller_id]) < limit:
            sellers[seller_id].append(product_id)

    if len(sellers) == 1:
        return list(sellers.values())[0]
    return sellers


def get_top_selling_products_for_sellers(limit=10):
    top_selling = get_top_selling_products()
    sellers = group_products_by_seller(top_selling, "top_selling", limit)

    result = {}
    for seller_id, product_ids in sellers.items():
        top_selling_products = get_products_by_ids(product_ids)
        result[seller_id] = ProductSerializer(top_selling_products, many=True).data

    return result


def get_top_rated_products_for_sellers(limit=10):
    top_rated = get_top_rated_products()
    sellers = group_products_by_seller(top_rated, "top_rated", limit)

    result = {}
    for seller_id, product_ids in sellers.items():
        top_rated_products = get_products_by_ids(product_ids)
        result[seller_id] = ProductSerializer(top_rated_products, many=True).data

    return result
