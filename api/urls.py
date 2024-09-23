from django.urls import path, include


from api.views.category import (
    CategoryListView,
    CreateCategoryView,
    CategoryDetailView,
    CategoryUpdateView,
    CategoryDeleteView,
    CategoryProductListView,
)
from .views.order import (
    OrderListView,
    OrderCancelView,
    OrderTrackView,
    OrderCreateView,
    OrderDeliverView,
    OrderCreateViewWithDiscount,
)

from .views.cart import (
    AddToCartView,
    RemoveFromCartView,
    ClearCartView,
    UpdateCartItemView,
    CartView,
)

from .views import (
    UserRegisterView,
    UserLoginView,
    VerifyOTPView,
    RefreshTokenView,
    ForgotPasswordView,
    PasswordResetView,
    UpdatePasswordView,
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
from .views.report import ReportListView, ReportCreateView, ReportDetailView

from api.views.cart import (
    AddToCartView,
    RemoveFromCartView,
    ClearCartView,
    UpdateCartItemView,
    CartView,
)

from .views.product import (
    ProductListView,
    ProductDetailView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
)

from .views.review import (
    GetReviewsByProductView,
    CreateReviewView,
    UpdateReviewView,
    DeleteReviewView,
)

from .views.supplier import (
    SupplierCreateView,
    SupplierUpdateView,
    SupplierDeleteView,
    SupplierListView,
    SupplierDetailView,
)
from api.views.top import TopSellingProductsView, TopRatedProductsView
from api.views.discount import DiscountCreateView, DiscountListView

from api.views.sales import WeeklySalesView, DailySalesView, MonthlySalesView
from api.views.address import (
    AddressListView,
    AddressCreateView,
    AddressDetailView,
    AddressUpdateView,
    AddressDeleteView,
)

Address_patterns = [
    path("", AddressListView.as_view(), name="address_list"),
    path("new/", AddressCreateView.as_view(), name="address_create"),
    path("<int:pk>/", AddressDetailView.as_view(), name="address_detail"),
    path("<int:pk>/edit/", AddressUpdateView.as_view(), name="address_update"),
    path("<int:pk>/delete/", AddressDeleteView.as_view(), name="address_delete"),
]
category_patterns = [
    path("", CategoryListView.as_view(), name="list"),
    path("create/", CreateCategoryView.as_view(), name="create-category"),
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
    path("create/", OrderCreateView.as_view(), name="create"),
    path("<int:pk>/deliver/", OrderDeliverView.as_view(), name="deliver"),
    path(
        "create-with-discount/",
        OrderCreateViewWithDiscount.as_view(),
        name="create-with-discount",
    ),
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
    path("update-password/", UpdatePasswordView.as_view(), name="update-password"),
]

payment_patterns = [
    path("", PaymentListView.as_view(), name="payment-list"),
    path("create/", PaymentCreateView.as_view(), name="payment-create"),
    path("<int:payment_id>/", PaymentDetailView.as_view(), name="payment-detail"),
    path(
        "update/<int:payment_id>/", PaymentUpdateView.as_view(), name="payment-update"
    ),
    path(
        "delete/<int:payment_id>/", PaymentDeleteView.as_view(), name="payment-delete"
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
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"
    ),
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path(
        "update/<int:item_id>/", UpdateCartItemView.as_view(), name="update-cart-item"
    ),
]

product_patterns = [
    path("", ProductListView.as_view(), name="product-list"),
    path("<int:product_id>/", ProductDetailView.as_view(), name="product-detail"),
    path("create/", ProductCreateView.as_view(), name="product-create"),
    path(
        "update/<int:product_id>/", ProductUpdateView.as_view(), name="product-update"
    ),
    path(
        "delete/<int:product_id>/", ProductDeleteView.as_view(), name="product-delete"
    ),
]

cart_patterns = [
    path("", CartView.as_view(), name="cart"),
    path("add/", AddToCartView.as_view(), name="add-to-cart"),
    path(
        "remove/<int:item_id>/", RemoveFromCartView.as_view(), name="remove-from-cart"
    ),
    path("clear/", ClearCartView.as_view(), name="clear-cart"),
    path(
        "update/<int:item_id>/", UpdateCartItemView.as_view(), name="update-cart-item"
    ),
]

review_patterns = [
    path(
        "products/<int:product_id>/",
        GetReviewsByProductView.as_view(),
        name="product-reviews",
    ),
    path(
        "products/<int:product_id>/create/",
        CreateReviewView.as_view(),
        name="create-review",
    ),
    path("update/<int:review_id>", UpdateReviewView.as_view(), name="update-review"),
    path(
        "delete/<int:review_id>",
        DeleteReviewView.as_view(),
        name="delete-review",
    ),
]

supplier_patterns = [
    path("", SupplierListView.as_view(), name="supplier-list"),
    path("create/", SupplierCreateView.as_view(), name="supplier-create"),
    path("<int:supplier_id>/", SupplierDetailView.as_view(), name="supplier-detail"),
    path(
        "<int:supplier_id>/update/",
        SupplierUpdateView.as_view(),
        name="supplier-update",
    ),
    path(
        "<int:supplier_id>/delete/",
        SupplierDeleteView.as_view(),
        name="supplier-delete",
    ),
]
report_patterns = [
    path("reports/", ReportListView.as_view(), name="report-list"),
    path("reports/create/", ReportCreateView.as_view(), name="report-create"),
    path("reports/<int:pk>/", ReportDetailView.as_view(), name="report-detail"),
]
discount_patterns = [
    path("create/", DiscountCreateView.as_view(), name="create"),
    path("list/", DiscountListView.as_view(), name="list"),
]
sales_patterns = [
    path("daily/", DailySalesView.as_view(), name="daily-sales"),
    path("weekly/", WeeklySalesView.as_view(), name="weekly-sales"),
    path("monthly/", MonthlySalesView.as_view(), name="monthly-sales"),
]

urlpatterns = [
    path("categories/", include((category_patterns, "categories"))),
    path("orders/", include((order_patterns, "orders"))),
    path("users/", include(user_patterns)),
    path("payments/", include(payment_patterns)),
    path("wishlists/", include(wishlist_patterns)),
    path("reports/", include(report_patterns)),
    path("carts/", include(cart_patterns)),
    path("products/", include(product_patterns)),
    path("reviews/", include(review_patterns)),
    path("suppliers/", include(supplier_patterns)),
    path("discount/", include(discount_patterns)),
    path("address/", include(Address_patterns)),
    path(
        "top-selling-products/",
        TopSellingProductsView.as_view(),
        name="top-selling-products",
    ),
    path(
        "top-rated-products/",
        TopRatedProductsView.as_view(),
        name="top-rated-products",
    ),
    path("sales/", include(sales_patterns)),
]
