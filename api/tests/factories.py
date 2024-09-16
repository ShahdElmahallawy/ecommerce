import factory
from factory.django import DjangoModelFactory
from api.models import Product, Order, OrderItem, Review, Category
from api.models.payment import Payment
from api.models.user import User
from decimal import Decimal
from django.utils import timezone
from api.models.supplier import Supplier
from api.models.report import Report
from api.models.discount import Discount


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


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    payment_method = factory.SubFactory(PaymentFactory)
    status = factory.Iterator(["pending", "delivered", "cancelled"])
    total_price = Decimal("0.00")


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
    count = factory.Faker("random_int", min=1, max=100)
    currency = factory.Faker("random_element", elements=["USD", "EUR", "EGP"])
    created_by = factory.SubFactory(UserFactory)
    supplier = factory.SubFactory(SupplierFactory)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductFactory)
    quantity = factory.Faker("random_int", min=1, max=10)
    unit_price = factory.Faker(
        "pydecimal", left_digits=5, right_digits=2, positive=True
    )


class ReportFactory(DjangoModelFactory):
    class Meta:
        model = Report

    report_type = factory.Iterator(["product", "order"])
    rid = factory.Faker("random_int", min=1, max=1000)
    user = factory.SubFactory(UserFactory)
    message = factory.Faker("text")


class DiscountFactory(DjangoModelFactory):
    class Meta:
        model = Discount

    user = factory.SubFactory(UserFactory)
    code = factory.Faker("bothify", text="????-####")
    discount_percentage = factory.Faker(
        "pydecimal",
        left_digits=2,
        right_digits=2,
        positive=True,
        min_value=5,
        max_value=50,
    )
    start_date = factory.LazyFunction(timezone.now)
    end_date = factory.LazyFunction(
        lambda: timezone.now() + timezone.timedelta(days=30)
    )
    is_active = True


class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review

    user = factory.SubFactory(UserFactory)
    product = factory.SubFactory(ProductFactory)
    text = factory.Faker("paragraph")
    rating = factory.Faker("pyfloat", min_value=1, max_value=5, right_digits=1)


class CategoryFactory(DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Faker("word")
    featured_product = factory.SubFactory(
        "api.tests.factories.ProductFactory", name="Featured Product"
    )
