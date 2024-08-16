from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer, TokenRefreshSerializer
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import *
from accounts.tasks import send_otp_code_to_email
from accounts.utility import check_input_type, generate_code


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")

    def create(self, validated_data):
        user = User.objects.filter(email=validated_data.get("email"), is_active=False).first()
        if user is not None:
            try:
                sms = VerificationOtp.objects.get(
                    user=user,
                    type=VerificationOtp.VerificationType.REGISTER,
                    expires_in__lt=timezone.now(),
                    is_active=True
                )
                sms.expires_in = timezone.now() + settings.OTP_CODE_ACTIVATION_TIME
                code = generate_code()
                sms.code = code
                sms.save()
                send_otp_code_to_email(code=code, email=user.email)
            except VerificationOtp.DoesNotExist:
                pass  # No active OTP found, continue with the user creation/update
            user.set_password(validated_data.get('password'))
            user.save()
        else:
            user = User.objects.create(first_name=validated_data.get('first_name'),
                                       last_name=validated_data.get('last_name'),
                                       email=validated_data.get('email'))
            user.set_password(validated_data.get('password'))
            user.save()
        return user


class VerificationOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)
    verify_type = serializers.ChoiceField(choices=VerificationOtp.VerificationType,required=True)


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)


class ResetPasswordFinishSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    verification = serializers.IntegerField(required=True)
    password = serializers.CharField(required=True)
    password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs.get("password") != attrs.get("password_confirm"):
            raise serializers.ValidationError("Password and password_confirm not match")
        return attrs


class LoginSerializer(TokenObtainPairSerializer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'] = serializers.CharField(required=True)

    def auth_validate(self,data):
        email = data.get('email')
        if check_input_type(email) != "email":
            raise serializers.ValidationError("This not email")
        user = self.get_user(email__iexact=email)

        if not user.is_active:
            raise ValidationError("User is not active")

        user = authenticate(email=email, password=data['password'])

        if user is None:
            raise ValidationError("Email or password is not correct")
        self.user = user

    def validate(self, data):
        self.auth_validate(data)
        data = super().validate(data)
        return data

    def get_user(self, **kwargs):
        users = User.objects.filter(**kwargs)
        if not users.exists():
            raise ValidationError("No account found with this email")
        return users.first()


class LoginRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user)
        return data


class LogOutSerializer(serializers.Serializer):
    refresh = serializers.CharField()