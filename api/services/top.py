# from api.selectors.top import get_top_selling_products, get_top_rated_products
# from api.serializers import ProductSerializer
# from api.models.product import Product

# def get_products_grouped_by_seller(products, limit):
#     sellers = {}
#     for product in products:
#         seller_id = product['product__created_by'] if 'product__created_by' in product else product.created_by.id
#         product_id = product['product__id'] if 'product__id' in product else product.id
        
#         if seller_id not in sellers:
#             sellers[seller_id] = []
#         if len(sellers[seller_id]) < limit:
#             sellers[seller_id].append(product_id)
    
#     return sellers

# def get_products_by_seller(sellers, limit):
#     result = {}
#     product_ids = [product_id for product_list in sellers.values() for product_id in product_list]
#     products = Product.objects.filter(id__in=product_ids).select_related('created_by')

#     for seller_id, product_list in sellers.items():
#         seller_products = products.filter(created_by_id=seller_id)[:limit]
#         result[seller_id] = ProductSerializer(seller_products, many=True).data

#     return result

# def get_top_selling_products_for_sellers(limit=10):
#     top_selling = get_top_selling_products(limit)
#     sellers = get_products_grouped_by_seller(top_selling, limit)
#     return get_products_by_seller(sellers, limit)

# def get_top_rated_products_for_sellers(limit=10):
#     top_rated = get_top_rated_products(limit)
#     sellers = get_products_grouped_by_seller(top_rated, limit)
#     return get_products_by_seller(sellers, limit)


from django.db.models import Sum, Avg
from api.models import Product, OrderItem
from api.selectors.top import get_top_selling_products, get_top_rated_products, get_products_by_ids
from api.serializers import ProductSerializer

def get_top_selling_products(seller_id=None, limit=10):
    query = OrderItem.objects.values('product__id', 'product__name', 'product__created_by')
    if seller_id:
        query = query.filter(product__created_by=seller_id)
    
    top_selling = (
        query
        .annotate(total_sales=Sum('quantity'))
        .order_by('-total_sales')[:limit]
    )
    
    return group_products_by_seller(top_selling, 'top_selling', limit)

def get_top_rated_products(seller_id=None, limit=10):
    query = Product.objects.annotate(avg_rating=Avg('reviews__rating'))
    if seller_id:
        query = query.filter(created_by=seller_id)
    
    top_rated = query.order_by('-avg_rating')[:limit]
    
    return group_products_by_seller(top_rated, 'top_rated', limit)

def group_products_by_seller(products, product_key, limit):
    sellers = {}
    for product in products:
        seller_id = product['product__created_by'] if product_key == 'top_selling' else product.created_by.id
        product_id = product['product__id'] if product_key == 'top_selling' else product.id
        
        if seller_id not in sellers:
            sellers[seller_id] = []
        if len(sellers[seller_id]) < limit:
            sellers[seller_id].append(product_id)
    
    if len(sellers) == 1:
        return list(sellers.values())[0]
    return sellers

def get_top_selling_products_for_sellers(limit=10):
    top_selling = get_top_selling_products()
    sellers = group_products_by_seller(top_selling, 'top_selling', limit)

    result = {}
    for seller_id, product_ids in sellers.items():
        top_selling_products = get_products_by_ids(product_ids)
        result[seller_id] = ProductSerializer(top_selling_products, many=True).data

    return result

def get_top_rated_products_for_sellers(limit=10):
    top_rated = get_top_rated_products()
    sellers = group_products_by_seller(top_rated, 'top_rated', limit)

    result = {}
    for seller_id, product_ids in sellers.items():
        top_rated_products = get_products_by_ids(product_ids)
        result[seller_id] = ProductSerializer(top_rated_products, many=True).data

    return result