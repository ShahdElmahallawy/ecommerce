from api.models import User, Profile, Product, Review, Payment, Supplier
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
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

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "name",
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_type",
                ),
            },
        ),
    )

    list_filter = ["is_superuser", "is_staff", "is_active", "user_type"]
    search_fields = ["email", "name"]
    list_per_page = 10


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "phone", "preferred_currency"]
    search_fields = ["user__name", "phone"]
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
        "category",
        "currency",
        "created_by",
        "supplier",
    ]

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

    list_filter = ["category", "currency", "supplier", InventoryFilter]
    search_fields = ["name", "description"]
    list_editable = ["price", "count"]
    list_per_page = 10


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

    readonly_fields = ["pan", "cvv"]

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

    list_filter = ["card_type", "default"]
    search_fields = ["user__username", "bank_name", "pan"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        if obj.default and not change:
            Payment.objects.filter(user=obj.user).update(default=False)
        elif obj.default:
            Payment.objects.filter(user=obj.user).update(default=False)
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        if obj.default:
            raise Exception(
                "Cannot delete default payment, set another payment as default first"
            )
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

    list_filter = ["rating"]
    search_fields = ["user__username", "product__name", "text"]
    list_per_page = 10

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def delete_model(self, request, obj):
        super().delete_model(request, obj)
