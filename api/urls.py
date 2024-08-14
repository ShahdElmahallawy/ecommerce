from django.urls import path
from .views.category import category_list_view, category_detail_view, category_update_view, category_delete_view, category_product_List_view
from .views.order import order_cancel_View, order_track_view, order_list_view
urlpatterns = [
    path('categories/', category_list_view.as_view(), name='category-list'),
    path('categories/<int:pk>/', category_detail_view.as_view(), name='category-detail'),
    path('categories/<int:pk>/update/', category_update_view.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', category_delete_view.as_view(), name='category-delete'),
    path('categories/<int:category_pk>/products/', category_product_List_view.as_view(), name='category-products'),
    path('orders/', order_list_view.as_view(), name='order-list'),
    path('orders/<int:pk>/cancel/', order_cancel_View.as_view(), name='order-cancel'),
    path('orders/<int:pk>/track/', order_track_view.as_view(), name='order-track'),
]
