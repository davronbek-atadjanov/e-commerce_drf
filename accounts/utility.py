from django.core.exceptions import ValidationError


def check_otp_code(value):
        if len(value) != 6:
            raise ValidationError('OTP code must be 6 digits long')
