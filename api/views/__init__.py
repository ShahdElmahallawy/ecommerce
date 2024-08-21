from .user import (
    UserRegisterView,
    UserLoginView,
    RefreshTokenView,
    ForgotPasswordView,
    PasswordResetView,
)
from .profile import ProfileDetailView, ProfileUpdateView
from .payment import (
    PaymentListView,
    PaymentDetailView,
    PaymentCreateView,
    PaymentUpdateView,
    PaymentDeleteView,
)
from .wishlist import (
    WishlistListView,
    WishlistItemCreateView,
    WishlistItemDeleteView,
    WishlistDeleteView,
)
