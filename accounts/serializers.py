from rest_framework import serializers
from accounts.models import *


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "password")


class VerificationOtpSerializer(serializers.Serializer):
    code = serializers.IntegerField(required=True)
    email = serializers.CharField(required=True)

