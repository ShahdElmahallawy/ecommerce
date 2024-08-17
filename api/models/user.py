from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager


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
        email: Email of the user
        name: Name of the user
        otp_code: OTP code for user verification
        otp_created_at: Time when the OTP code was created
    """

    email = models.EmailField(max_length=255, unique=True)
    username = None
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    otp_code = models.CharField(max_length=6, null=True)
    otp_created_at = models.DateTimeField(null=True)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        """Return string representation of the user"""
        return self.email
