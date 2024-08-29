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


from .views import (
    UserRegisterView,
    UserLoginView,
    VerifyOTPView,
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
    path("verify-otp/", VerifyOTPView.as_view(), name="verify-otp"),
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
        "items/delete/<int:item_id>",
        WishlistItemDeleteView.as_view(),
        name="wishlist-item-delete",
    ),
    path("clear/", WishlistDeleteView.as_view(), name="wishlist-clear"),
]

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
    path("users/", include(user_patterns)),
    path("payments/", include(payment_patterns)),
    path("wishlists/", include(wishlist_patterns)),
    path("categories/", include((category_patterns, "categories"))),
    path("orders/", include((order_patterns, "orders"))),
    path("cart/", include((cart_patterns, "cart"))),
    path("products/", include((product_patterns, "products"))),
]
