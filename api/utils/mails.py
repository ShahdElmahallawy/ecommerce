from django.core.mail import send_mail
from django.conf import settings
from smtplib import SMTPException


class EmailService:
    def __init__(self, user):
        self.user = user

    def send_email(self, subject, message):
        """
        Sends an email to the user with the specified subject and message.
        """
        try:
            send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [self.user.email],
                fail_silently=False,
            )
        except SMTPException:
            raise SMTPException("Failed to send email. Please try again later.")

    def send_password_reset_email(self, reset_link):
        """
        Sends a password reset email to the user with the reset link.
        """
        subject = "Password Reset Request"
        message = (
            f"Hi {self.user.name},\n\n"
            "You requested a password reset. Click the link below to reset your password:\n\n"
            f"{reset_link}\n\n"
            "If you did not request this reset, please ignore this email."
        )
        self.send_email(subject, message)

    def send_otp_email(self, otp):
        """
        Sends an OTP email to the user.
        """
        subject = "OTP Verification (Expires in 5 minutes)"
        message = (
            f"Hi {self.user.name},\n\n"
            "Here is your OTP code for verification:\n\n"
            f"{otp}\n\n"
            "This code will expire in 5 minutes.\n\n"
            "If you did not request this OTP, please change your password immediately."
        )
        self.send_email(subject, message)
