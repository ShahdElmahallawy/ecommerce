from django.urls import reverse
from django.contrib import messages
from django.shortcuts import redirect
from django.utils.html import format_html
from api.models import User, Profile, Product, Review, Payment, Supplier
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from api.models.discount import Discount
from api.models import OrderItem, Order, Review
from api.models.report import Report
from api.models.product import Product
from api.models.payment import Payment
from api.models.user import User


from django.db.models.query import QuerySet


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Define the admin pages for users."""

    ordering = ["id"]
    list_display = [
        "email",
        "name",
        "is_superuser",
        "is_staff",
        "is_active",
        "user_type",
    ]

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal Info", {"fields": ("name",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login",)}),
    )

    readonly_fields = ["last_login"]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "user",
        "discount_percentage",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active", "start_date", "end_date")
    search_fields = ("code", "user__email", "discount_percentage")
    readonly_fields = ("created_at", "updated_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "product", "quantity", "unit_price")
    list_filter = ("order__status",)
    search_fields = ("order__id", "product__name")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "status", "total_price", "payment_method")
    list_filter = ("status",)
    search_fields = ("id", "user__email")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ("id", "report_type", "rid", "user", "message")
    list_filter = ("report_type",)
    search_fields = ("user__email", "message")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "preferred_currency"]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "phone",
                    "preferred_currency",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "phone",
                    "preferred_currency",
                ),
            },
        ),
    )

    search_fields = ["user__name", "phone"]
    list_select_related = ["user"]
    autocomplete_fields = ["user"]
    list_filter = ["preferred_currency"]
    list_display_links = ["user"]
    list_per_page = 10


class InventoryFilter(admin.SimpleListFilter):
    title = "count"
    parameter_name = "count"

    def lookups(self, request, model_admin):
        return [("<5", "Low")]

    def queryset(self, request, queryset: QuerySet):
        if self.value() == "<5":
            print("filtering")
            return queryset.filter(count__lt=5)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """Define the admin pages for products."""

    ordering = ["id"]
    list_display = [
        "name",
        "price",
        "description",
        "count",
        "category_name",
        "currency",
        "created_by",
        "supplier_name",
        "thumbnail",
    ]

    def thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "name",
                    "price",
                    "description",
                    "image",
                    "count",
                    "category",
                    "currency",
                    "created_by",
                    "supplier",
                )
            },
        ),
    )
    readonly_fields = ["created_by"]
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "price",
                    "description",
                    "image",
                    "count",
                    "category",
                    "currency",
                    "created_by",
                    "supplier",
                ),
            },
        ),
    )

    list_filter = ["category", "supplier", "created_by", InventoryFilter]
    search_fields = ["name", "description"]
    autocomplete_fields = ["supplier"]
    list_editable = ["price", "count"]
    list_select_related = ["category", "created_by", "supplier"]
    list_per_page = 10

    def category_name(self, product):
        if product.category:
            return product.category.name

    def supplier_name(self, product):
        if product.supplier:
            return product.supplier.name

    def created_by(self, product):
        if product.created_by:
            return product.created_by.name


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Define the admin pages for payments."""

    ordering = ["id"]
    list_display = [
        "user",
        "pan",
        "bank_name",
        "expiry_date",
        "cvv",
        "card_type",
        "default",
    ]

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "pan",
                    "bank_name",
                    "expiry_date",
                    "cvv",
                    "card_type",
                    "default",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "pan",
                    "bank_name",
                    "expiry_date",
                    "cvv",
                    "card_type",
                    "default",
                ),
            },
        ),
    )
    list_select_related = ["user"]
    autocomplete_fields = ["user"]
    list_filter = ["card_type", "default"]
    search_fields = ["user__username", "bank_name", "pan"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):

        if obj.default:
            Payment.objects.filter(user=obj.user).update(default=False)

        if not Payment.objects.filter(user=obj.user, default=True).exists():
            obj.default = True

        if Payment.objects.filter(user=obj.user).count() == 1:
            obj.default = True
            messages.warning(
                request, "The only payment method cannot be unset as the default."
            )
            messages.set_level(request, messages.WARNING)

        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.default:
            messages.error(
                request,
                "Cannot delete default payment, set another payment as default first",
            )
            messages.set_level(request, messages.ERROR)
            return redirect(reverse("admin:api_payment_change", args=[obj.pk]))
        super().delete_model(request, obj)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "name",
        "email",
    ]

    fieldsets = ((None, {"fields": ("name", "email")}),)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "name",
                    "email",
                ),
            },
        ),
    )

    search_fields = ["name", "email"]
    list_per_page = 10


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    ordering = ["id"]
    list_display = [
        "user",
        "product",
        "rating",
        "text",
    ]

    fieldsets = ((None, {"fields": ("user", "product", "text", "rating")}),)

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "user",
                    "product",
                    "text",
                    "rating",
                ),
            },
        ),
    )
    list_select_related = ["user", "product"]
    autocomplete_fields = ["user", "product"]
    list_filter = ["rating"]
    search_fields = ["user__username", "product__name", "text"]
    list_per_page = 10
