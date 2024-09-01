from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager
from api.constants import USER_TYPES


class UserManager(BaseUserManager):
    """Manager for custom user model"""

    def create_user(self, email, name, password=None, **extra_fields):
        """Create and return a new user"""
        if not email:
            raise ValueError("User must have an email address")

        email = self.normalize_email(email)
        user = self.model(email=email, name=name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and return a new superuser"""
        user = self.create_user(email, name, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractUser, PermissionsMixin):
    """Custom user model that supports using email instead of username

    Fields:
        email: Email address of the user
        name: Name of the user
        is_active: Boolean flag to indicate if the user is active
        is_staff: Boolean flag to indicate if the user is staff
        reset_password_token: Token used to reset the user's password
        reset_password_token_expiry: Expiry date for the reset password token
        password_changed_at: Date when the user last changed their password
        otp_code: One-time password code used for two-factor authentication
    """

    email = models.EmailField(max_length=255, unique=True)
    username = None
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    reset_password_token = models.CharField(max_length=255, null=True, unique=True)
    reset_password_token_expiry = models.DateTimeField(null=True)
    password_changed_at = models.DateTimeField(null=True)
    otp_code = models.CharField(max_length=6, null=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default="customer")

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        """Return string representation of the user"""
        return self.email
