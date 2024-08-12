from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from accounts.models import *
from accounts.serializers import *


class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class VerificationOtpView(CreateAPIView):
    queryset = VerificationOtp.objects.all()
    serializer_class = VerificationOtpSerializer

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = User.objects.get(email=data.get("email"))
        except User.DoesNotExist:
            raise APIException(detail="User not found")

        sms = VerificationOtp.objects.filter(
            Q(user=user) & Q(type=VerificationOtp.VerificationType.REGISTER) & Q(code=data.get("code"))
        )

        if not sms.exists():
            return Response(data={"detail": "Otp code not found"}, status=status.HTTP_400_BAD_REQUEST)

        if not sms.filter(expires_in__gt=timezone.now()):
            return Response(data={"detail": "Otp code expired"}, status=status.HTTP_400_BAD_REQUEST)

        sms_obj = sms.last()
        user.is_active = True
        user.save()
        sms_obj.is_active = False
        sms_obj.save()

        return Response(data={"message": "otp_code_is_activated"}, status=status.HTTP_200_OK)
