from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import (
    UserRegisterView,
    PasswordResetRequestView,
    PasswordResetView,
    ProfileDetailView,
    ProfileUpdateView,
    PaymentListView,
    PaymentDetailView,
    PaymentCreateView,
    PaymentUpdateView,
    PaymentDeleteView,
)


user_patterns = [
    path("register/", UserRegisterView.as_view(), name="user-register"),
    path("password-reset/", PasswordResetRequestView.as_view(), name="password-reset"),
    path(
        "password-reset/confirm/<str:token>/",
        PasswordResetView.as_view(),
        name="password-reset-confirm",
    ),
    path("login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("refresh-token/", TokenRefreshView.as_view(), name="token-refresh"),
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

urlpatterns = [
    path("users/", include(user_patterns)),
    path("payments/", include(payment_patterns)),
]
