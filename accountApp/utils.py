import random
from django.core.mail import send_mail
from .models import EmailOTP
from datetime import datetime

def generate_otp():
    return str(random.randint(100000, 999999))

def send_otp_email(user):
    otp = generate_otp()

    # Save OTP for this user (update if exists)
    obj, created = EmailOTP.objects.update_or_create(
        user=user,
        defaults={'otp': otp, 'created_at': datetime.now()}
    )

    subject = "Your OTP Code"
    message = f"Your OTP code is {otp}. It is valid for 10 minutes."
    from_email = "emailtesting269@gmail.com"
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

    return otp
