from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException


def send_password_reset_email(user, reset_link):
    """
    Sends a password reset email to the user with reset link.
    """
    subject = "Password Reset Request"
    message = f"Hi {user.name},\n\n"
    message += "You requested a password reset. Click the link below to reset your password:\n\n"
    message += f"{reset_link}\n\n"
    message += "If you did not request this reset, please ignore this email."
    try:
        res = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except:
        raise SMTPException(
            "Failed to send password reset email. Please try again later."
        )


def send_otp_email(user, otp):
    """
    Sends an OTP email to the user.
    """
    subject = "OTP Verification (Expires in 5 minutes)"
    message = f"Hi {user.name},\n\n"
    message += "Here is your OTP code for verification:\n\n"
    message += f"{otp}\n\n"
    message += "This code will expire in 5 minutes."
    message += (
        "If you did not request this OTP, please change your password immediately."
    )
    try:
        res = send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )
    except:
        raise SMTPException("Failed to send OTP email. Please try again later.")
