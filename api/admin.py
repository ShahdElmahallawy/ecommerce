from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Profile

# Register your models here.


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ["id"]
    list_display = ["email", "name"]


admin.site.register(Profile)


class ProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "type", "address", "phone", "preferred_currency"]
