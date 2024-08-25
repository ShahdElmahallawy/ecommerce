from django.urls import path, include

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
    path("users/", include(user_patterns)),
    path("payments/", include(payment_patterns)),
    path("wishlists/", include(wishlist_patterns)),
]
