from django.urls import path, include

from .views.category import (
    CategoryListView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryProductListView,
)
from .views.order import OrderListView, OrderCancelView, OrderTrackView, OrderCreateView

from .views import (
    UserRegisterView,
    UserLoginView,
    RefreshTokenView,
    ForgotPasswordView,
    PasswordResetView,
    ProfileDetailView,
    ProfileUpdateView,
    PaymentListView,
    PaymentDetailView,
    PaymentCreateView,
    PaymentUpdateView,
    PaymentDeleteView,
    WishlistListView,
    WishlistItemCreateView,
    WishlistItemDeleteView,
    WishlistDeleteView,
)

category_patterns = [
    path("", CategoryListView.as_view(), name="list"),
    path("<int:pk>/", CategoryDetailView.as_view(), name="detail"),
    path("<int:pk>/update/", CategoryUpdateView.as_view(), name="update"),
    path("<int:pk>/delete/", CategoryDeleteView.as_view(), name="delete"),
    path(
        "<int:category_pk>/products/",
        CategoryProductListView.as_view(),
        name="products",
    ),
]
order_patterns = [
    path("", OrderListView.as_view(), name="list"),
    path("<int:pk>/cancel/", OrderCancelView.as_view(), name="cancel"),
    path("<int:pk>/track/", OrderTrackView.as_view(), name="track"),
    path("orders/create/", OrderCreateView.as_view(), name="create"),
]

user_patterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("forgot-password/", ForgotPasswordView.as_view(), name="forgot-password"),
    path(
        "password-reset/<str:token>/",
        PasswordResetView.as_view(),
        name="password-reset",
    ),
    path("login/", UserLoginView.as_view(), name="user-login"),
    path("refresh-token/", RefreshTokenView.as_view(), name="refresh-token"),
    path("me/", ProfileDetailView.as_view(), name="profile-detail"),
    path("me/update/", ProfileUpdateView.as_view(), name="profile-update"),
]

payment_patterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("create/", PaymentCreateView.as_view(), name="payment-create"),
    path("<int:payment_id>/", PaymentDetailView.as_view(), name="payment-detail"),
    path(
        "<int:payment_id>/update/", PaymentUpdateView.as_view(), name="payment-update"
    ),
    path(
        "<int:payment_id>/delete/", PaymentDeleteView.as_view(), name="payment-delete"
    ),
]

wishlist_patterns = [
    path("", WishlistListView.as_view(), name="wishlist-list"),
    path(
        "items/create/", WishlistItemCreateView.as_view(), name="wishlist-item-create"
    ),
    path(
        "items/delete/<int:product_id>",
        WishlistItemDeleteView.as_view(),
        name="wishlist-item-delete",
    ),
    path("clear/", WishlistDeleteView.as_view(), name="wishlist-clear"),
]

urlpatterns = [
    path("categories/", include((category_patterns, "categories"))),
    path("orders/", include((order_patterns, "orders"))),
    path("users/", include(user_patterns)),
    path("payments/", include(payment_patterns)),
    path("wishlists/", include(wishlist_patterns)),
]
