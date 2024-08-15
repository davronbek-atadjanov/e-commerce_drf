from django.utils import timezone
from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from .managers import UserManager
from .utility import check_otp_code


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=15,
                                    validators=[RegexValidator(r'^\+?1?\d{9,13}$')], null=True, blank=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    is_active = models.BooleanField(_("active"), default=False,
                                    help_text=_(
                                        "Designates whether this user should be treated as active. "
                                        "Unselect this instead of deleting accounts."),)
    is_staff = models.BooleanField(_('staff status'), default=False,
                                   help_text=_('Designates whether the user can log into this admin site.'))
    is_superuser = models.BooleanField(_('superuser status'), default=False,
                                       help_text=_('Designates whether the user is a superuser.'))
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)
    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    objects = UserManager()

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='custom_user_set',  # related_name ni o'zgartirish
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='custom_user_permission_set',  # related_name ni o'zgartirish
        help_text=_('Specific permissions for this user.'),
    )

    def __str__(self):
        return self.email

    def get_short_name(self):
        return self.first_name

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class VerificationOtp(models.Model):
    class VerificationType(models.TextChoices):
        REGISTER = "register", _("register")
        RESET_PASSWORD = "reset_password", _("reset password")
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name="verification_otp")
    code = models.IntegerField(_('Verification Code'), validators=[check_otp_code])
    type = models.CharField(_("Verification Type"), max_length=20, choices=VerificationType.choices)
    expires_in = models.DateTimeField(_("expires in "))
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.email} | code: {self.code}"

    class Meta:
        verbose_name = _("Verification OTP")
        verbose_name_plural = _("Verification OTPs")
        ordering = ["-expires_in"]


class UserAddress(models.Model):
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE, related_name="user_addresses")
    name = models.CharField(_("Name"), max_length=120)
    phone_number = models.CharField(_("Phone number"), max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,13}$')])
    apartment = models.CharField(_("Apartment"), max_length=120)
    street = models.TextField(_("Street"))
    pin_code = models.CharField(_("Pin code"), max_length=60)
    # city = models.ForeignKey()

    def __str__(self):
        return f"{self.user.id} {self.name}"

    class Meta:
        verbose_name = _("user address")
        verbose_name_plural = _('user addresses')
