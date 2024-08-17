from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView

from .views import UserRegisterView, UserProfileView, UserProfileView


urlpatterns = [
    path("users/register/", UserRegisterView.as_view(), name="user-register"),
    path("users/login/", TokenObtainPairView.as_view(), name="token-obtain-pair"),
    path("users/refresh-token/", TokenRefreshView.as_view(), name="token-refresh"),
    path("users/me/", UserProfileView.as_view(), name="user-profile"),
]
