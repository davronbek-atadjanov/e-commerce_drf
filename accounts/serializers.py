from rest_framework import serializers
from accounts.models import *


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


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
