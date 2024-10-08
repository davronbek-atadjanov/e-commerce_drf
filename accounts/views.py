from django.db.models import Q
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.models import *
from accounts.serializers import *
from accounts.utility import generate_code
from core.settings import OTP_CODE_ACTIVATION_TIME
from accounts.tasks import send_otp_code_to_email


class UserCreateView(CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


# class VerificationOtpView(CreateAPIView):
#     queryset = VerificationOtp.objects.all()
#     serializer_class = VerificationOtpSerializer
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.get(email=data.get("email"))
#         except User.DoesNotExist:
#             raise APIException(detail="User not found")
#         verify_type = data.get("verify_type")
#         sms = VerificationOtp.objects.filter(
#             Q(user=user) & Q(type=verify_type) & Q(code=data.get("code"))
#         )
#         if not sms.exists():
#             return Response(data={"detail": "Otp code not found"}, status=status.HTTP_400_BAD_REQUEST)
#
#         if not sms.filter(expires_in__gt=timezone.now()):
#             return Response(data={"detail": "Otp code expired"}, status=status.HTTP_400_BAD_REQUEST)
#
#         sms_obj = sms.last()
#         user.is_active = True
#         user.save()
#         sms_obj.is_active = False
#         sms_obj.save()
#         return Response({
#             'message': 'otp_code_is_activated',
#             "verification": sms_obj.id
#         }, status=status.HTTP_200_OK)


class VerifyOtpView(APIView):
    serializer_class = VerificationOtpSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = VerificationOtpSerializer(data=data)
            if not serializer.is_valid():
                raise APIException(detail="Data is not valid")
            user = User.objects.get(email=data.get("email"))
            verify_type = data.get("verify_type")
            sms = VerificationOtp.objects.filter(
                Q(user=user) &
                Q(type=verify_type) &
                Q(code=data.get("code"))
            )
            if not sms.exists():
                return Response(data={"message": "otp_code_not_found"}, status=status.HTTP_400_BAD_REQUEST)

            if not sms.filter(is_active=True).exists():
                return Response(data={"message": "otp_code_already_activated"}, status=status.HTTP_400_BAD_REQUEST)

            if not sms.filter(expires_in__gte=timezone.now()):
                return Response(data={"message": "otp_code_expired"}, status=status.HTTP_400_BAD_REQUEST)

            sms_obj = sms.last()
            user.is_active = True
            user.save()
            sms_obj.is_active = False
            sms_obj.save()
            user.refresh_from_db()
            return Response(data={"message": "otp_code_activated", "verification": sms_obj.id})

        except User.DoesNotExist:
            raise APIException(detail="User does not exist")

        except Exception as e:
            raise e


class ResetPasswordStartView(APIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ResetPasswordSerializer(data=data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=data.get("email"))
            code = generate_code()
            VerificationOtp.objects.create(user=user, code=code, type=VerificationOtp.VerificationType.RESET_PASSWORD,
                                           expires_in=timezone.now() + timezone.timedelta(minutes=OTP_CODE_ACTIVATION_TIME))
            send_otp_code_to_email(code=code, email=user.email)
            print("Send otp code")
            return Response(data={"message": "Otp code is sent to your email"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise APIException(detail="User not found")

        except Exception as e:
            raise e

# class ResetPasswordView(CreateAPIView):
#     serializer_class = ResetPasswordSerializer
#
#     def create(self, request, *args, **kwargs):
#         data = request.data
#         serializer = self.get_serializer(data=data)
#         if not serializer.is_valid():
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         try:
#             user = User.objects.get(email=data.get("email"))
#         except User.DoesNotExist:
#             raise APIException(detail="User not found")
#         code = generate_code()
#         VerificationOtp.objects.create(user=user, type=VerificationOtp.VerificationType.RESET_PASSWORD, code=code,
#                                        expires_in=timezone.now() + timezone.timedelta(minutes=OTP_CODE_ACTIVATION_TIME))
#         send_email(code=code, email=user.email)
#         print("Signal is working")
#         return Response(data={"message": "Otp code is sent to your email"}, status=status.HTTP_200_OK)


class ResetPasswordFinishView(APIView):
    serializer_class = ResetPasswordFinishSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = ResetPasswordFinishSerializer(data=data)
            if not serializer.is_valid():
                return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            user = User.objects.get(email=data.get("email"))
            sms = VerificationOtp.objects.get(
                Q(user=user) & Q(type=VerificationOtp.VerificationType.RESET_PASSWORD) & Q(id=data.get("verification"))
            )
            if sms.is_active is True:
                return Response(data={"detail": "otp_code_is_activated_yet"}, status=status.HTTP_400_BAD_REQUEST)
            user.set_password(data.get("password"))
            user.save()
            return Response(data={"message": "Password is reset successfully"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            raise APIException(detail="User not found")
        except VerificationOtp.DoesNotExist:
            raise APIException(detail="Otp code not found")
        except Exception as e:
            raise e


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LoginRefreshView(TokenRefreshView):
    serializer_class = LoginRefreshSerializer


class LogOutView(APIView):
    serializer_class = LogOutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        try:
            refresh_token = self.request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            data = {
                "success": True,
                "message": "You are loggout out"
            }
            return Response(data, status=206)
        except TokenError:
            return Response(status=400)


class UserAddressCreateView(CreateAPIView, ListAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = CreateUserAddressSerializers
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return UserAddress.objects.filter(user=self.request.user)


class UserAddressUpdateView(UpdateAPIView):
    queryset = UserAddress.objects.all()
    serializer_class = CreateUserAddressSerializers
    permission_classes = [IsAuthenticated]

