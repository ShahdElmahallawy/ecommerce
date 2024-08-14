from django.urls import path
from .views.category import CategoryListView, CategoryDetailView, CategoryUpdateView, CategoryDeleteView, CategoryProductListView
from .views.order import OrderCancelView, OrderTrackView, OrderListView

urlpatterns = [
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', CategoryDetailView.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', CategoryDeleteView.as_view(), name='category-delete'),
    path('categories/<int:category_pk>/products/', CategoryProductListView.as_view(), name='category-products'),
    path('orders/', OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/cancel/', OrderCancelView.as_view(), name='order-cancel'),
    path('orders/<int:pk>/track/', OrderTrackView.as_view(), name='order-track'),
]
