import factory
from django.contrib.auth import get_user_model
from factory.django import DjangoModelFactory
from api.models.supplier import Supplier
from api.models.product import Product
from api.models.wishlist import Wishlist
from api.models.wishlist_item import WishlistItem
from api.models.payment import Payment
from api.models.cart import Cart
from api.models.cart_item import CartItem
from api.models.profile import Profile

User = get_user_model()


class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
        skip_postgeneration_save = True

    email = factory.Faker("email")
    name = factory.Faker("name")
    password = factory.PostGenerationMethodCall("set_password", "defaultpassword")
    is_active = True
    is_staff = False
    user_type = factory.Faker("random_element", elements=["customer", "seller"])


class SupplierFactory(DjangoModelFactory):
    class Meta:
        model = Supplier

    name = factory.Faker("company")
    email = factory.Faker("email")


class ProductFactory(DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker("word")
    price = factory.Faker("pyfloat", left_digits=2, right_digits=2, positive=True)
    description = factory.Faker("sentence")
    image = factory.django.ImageField(filename="test_image.jpg")
    count = factory.Faker("random_int", min=1, max=100)
    currency = factory.Faker("random_element", elements=["USD", "EUR", "EGP"])
    created_by = factory.SubFactory(UserFactory)
    supplier = factory.SubFactory(SupplierFactory)


class WishlistFactory(DjangoModelFactory):
    class Meta:
        model = Wishlist

    user = factory.SubFactory(UserFactory)


class WishlistItemFactory(DjangoModelFactory):
    class Meta:
        model = WishlistItem

    wishlist = factory.SubFactory(WishlistFactory)
    product = factory.SubFactory(ProductFactory)


class PaymentFactory(DjangoModelFactory):
    class Meta:
        model = Payment

    user = factory.SubFactory(UserFactory)
    pan = factory.Faker("credit_card_number")
    bank_name = factory.Faker("company")
    expiry_date = factory.Faker("credit_card_expire")
    cvv = factory.Faker("random_number", digits=3)
    card_type = factory.Faker("random_element", elements=["credit", "debit"])
    default = factory.Faker("boolean")


class CartFactory(DjangoModelFactory):
    class Meta:
        model = Cart

    user = factory.SubFactory(UserFactory)


from api.models.cart_item import CartItem


class CartItemFactory(DjangoModelFactory):
    class Meta:
        model = CartItem

    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
    cart = factory.SubFactory(CartFactory)


class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    phone = factory.Faker("phone_number")
    preferred_currency = factory.Faker("random_element", elements=["USD", "EUR", "GBP"])
