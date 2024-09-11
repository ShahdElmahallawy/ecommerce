from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile
from django.contrib import admin
from api.models.discount import Discount
from api.models import OrderItem, Order, Review
from api.models.report import Report
from api.models.product import Product
from api.models.payment import Payment
from api.models.user import User

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]


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


admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "address", "phone", "preferred_currency"]
