from django.utils.timezone import datetime, timedelta

from django.db.models.signals import post_save

from django.dispatch import receiver

from accounts.models import User, VerificationOtp
from accounts.tasks import send_otp_code_to_email
from accounts.utility import generate_code
from core.settings import OTP_CODE_ACTIVATION_TIME


@receiver(post_save, sender=User)
def create_verification_otp(sender, instance, created, **kwargs):
    if created:
        code = generate_code()
        VerificationOtp.objects.create(user=instance, type=VerificationOtp.VerificationType.REGISTER, code=code,
                                       expires_in = datetime.now() + timedelta(minutes=OTP_CODE_ACTIVATION_TIME))
        send_otp_code_to_email(code=code, email=instance.email)
        print("Signal is working")


