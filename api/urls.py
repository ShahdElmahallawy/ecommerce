from django.contrib import admin
from django.urls import path, include
from api.views.cart_view import (
    CreateCartView,
    DeleteCartView,
    CheckoutCartView,
    ListCartView,
    TotalPriceCartView,
)
from api.views.product_view import (
    ListProductsView,
    RetrieveProductView,
    UpdateProductView,
    DeleteProductView,
    CreateProductView,
)

cart_patterns = [
    path("", ListCartView.as_view(), name="list-cart"),
    path("<int:pk>/", DeleteCartView.as_view(), name="remove-from-cart"),
    path("total/", TotalPriceCartView.as_view(), name="total-cart"),
    path("checkout/", CheckoutCartView.as_view(), name="checkout-cart"),
    path("create/", CreateCartView.as_view(), name="add-to-cart"),
]

product_patterns = [
    path("", ListProductsView.as_view(), name="product-list"),
    path("<int:pk>/", RetrieveProductView.as_view(), name="product-detail"),
    path("<int:pk>/update/", UpdateProductView.as_view(), name="update-product"),
    path("<int:pk>/delete/", DeleteProductView.as_view(), name="delete-product"),
    path("create/", CreateProductView.as_view(), name="create-product"),
]

urlpatterns = [
    path("cart/", include((cart_patterns, "cart"))),
    path("products/", include((product_patterns, "products"))),
]
