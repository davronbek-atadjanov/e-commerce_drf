from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from accounts.views import UserCreateView, VerifyOtpView, ResetPasswordStartView, ResetPasswordFinishView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("login/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("password-reset/start/", ResetPasswordStartView.as_view(), name="password_reset_start"),
    path("password-reset/finish/", ResetPasswordFinishView.as_view(), name="password_reset_finish"),
]