from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserCreateView, VerificationOtpView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("verify-otp/", VerificationOtpView.as_view(), name="verify-otp"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]