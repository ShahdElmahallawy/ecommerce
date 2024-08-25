"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin

from django.urls import path
from api.views.cart_view import (
    CreateCartView,
    DeleteCartView,
    CheckoutCartView,
    ListCartView,
    TotalPriceCartView,
)
from api.views.product_view import ListProductsView, RetrieveProductView, UpdateProductView, DeleteProductView, CreateProductView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/cart/", CreateCartView.as_view(), name="add-to-cart"),
    path("api/cart/<int:pk>/", DeleteCartView.as_view(), name="remove-from-cart"),
    path("api/cart/", ListCartView.as_view(), name="list-cart"),
    path("api/cart/total/", TotalPriceCartView.as_view(), name="total-cart"),
    path("api/cart/checkout/", CheckoutCartView.as_view(), name="checkout-cart"),
    path("api/products/", ListProductsView.as_view(), name="product-list"),
    path("api/products/<int:pk>/", RetrieveProductView.as_view(), name="product-detail"),
    path("api/products/<int:pk>/update/", UpdateProductView.as_view(), name="update-product"),
    path("api/products/<int:pk>/delete/", DeleteProductView.as_view(), name="delete-product"),
    path('api/products/create/', CreateProductView.as_view(), name='create-product'),

]

