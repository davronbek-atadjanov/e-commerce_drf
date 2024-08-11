from django.urls import path

from accounts.views import UserCreateView

urlpatterns = [
    path("register/", UserCreateView.as_view(), name="register"),
]