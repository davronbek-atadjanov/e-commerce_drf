import secrets
import re
from django.core.exceptions import ValidationError

from core.settings.base import EMAIL_HOST
email_regex = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b')

def check_otp_code(value):
        if len(value) != 6:
            raise ValidationError('OTP code must be 6 digits long')


def generate_code():
    numbers = "123456789"
    return "".join(secrets.choice(numbers) for _ in range(6))


def check_input_type(email):
    if re.fullmatch(email_regex, email):
        email = "email"
    else:
        data = {
            "success": False,
            "message": "Email noto'g'ri kiritilgan"
        }
        raise ValidationError(data)
    return email