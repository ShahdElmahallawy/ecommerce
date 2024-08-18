from django.core.mail import send_mail
from django.conf import settings


def send_password_reset_email(user, reset_link):
    """
    Sends a password reset email to the user with reset link.
    """
    subject = "Password Reset Request"
    message = f"Hi {user.name},\n\n"
    message += "You requested a password reset. Click the link below to reset your password:\n\n"
    message += f"{reset_link}\n\n"
    message += "If you did not request this reset, please ignore this email."

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )
