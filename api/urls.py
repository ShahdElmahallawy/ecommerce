from django.urls import path, include
from .views.category import (
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryProductListView,
)
from .views.order import (
    OrderListView,
    OrderCancelView,
    OrderTrackView,
)

category_patterns = [
    path('', CategoryListView.as_view(), name='list'),
    path('<int:pk>/', CategoryDetailView.as_view(), name='detail'),
    path('<int:pk>/update/', CategoryUpdateView.as_view(), name='update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='delete'),
    path('<int:category_pk>/products/', CategoryProductListView.as_view(), name='products'),
]
order_patterns = [
    path('', OrderListView.as_view(), name='list'),
    path('<int:pk>/cancel/', OrderCancelView.as_view(), name='cancel'),
    path('<int:pk>/track/', OrderTrackView.as_view(), name='track'),
]

urlpatterns = [
    path('categories/', include((category_patterns, 'categories'))),
    path('orders/', include((order_patterns, 'orders'))),
]
