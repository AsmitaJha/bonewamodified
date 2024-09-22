from django.contrib import admin
from django.urls import path, include

from .api import *
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("register-user", RegisterViewSet, basename="register-user")
router.register("logout-user", LogOutViewSet, basename="logout-user")
router.register("token/", OurTokenObtainPairViewSet, basename="token")

urlpatterns = [
    path("", include(router.urls)),
    path("login/", user_login, name="login"),
    path("password_reset/", password_reset_mail, name="password-reset"),
    path("password_change/<str:token>/", password_change, name="password-change"),
    path("send-mail/", send_email, name="send_email"),
    path("verify_otp/", otp_verification, name="verify_otp"),
]
