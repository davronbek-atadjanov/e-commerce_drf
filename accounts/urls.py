from django.urls import path
from accounts.views import UserCreateView, VerifyOtpView, ResetPasswordStartView, \
    ResetPasswordFinishView, LoginView, LoginRefreshView, LogOutView

# CustomLoginView,


urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
    path("verify-otp/", VerifyOtpView.as_view(), name="verify-otp"),
    path("login/", LoginView.as_view(), name="login"),
    path("login/refresh/", LoginRefreshView.as_view(), name="token_refresh"),
    path("logout/", LogOutView.as_view(), name="logout"),
    path("password-reset/start/", ResetPasswordStartView.as_view(), name="password_reset_start"),
    path("password-reset/finish/", ResetPasswordFinishView.as_view(), name="password_reset_finish"),
]