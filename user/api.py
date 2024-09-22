from rest_framework import viewsets
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny
# for otp generation
import datetime
import random
from base64 import urlsafe_b64encode
from datetime import timedelta

import jwt
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.exceptions import ObjectDoesNotExist

# for console backend
from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from rest_framework import filters, generics, mixins, response, status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view
from rest_framework.exceptions import ValidationError
from rest_framework.generics import GenericAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from . import serializers
from .models import (
    OTP,
    User,
)
from .serializers import (
    OTPCheckSerializer,
    OurTokenObtainPairSerializer,
    PasswordChangeSerializer,
    PasswordResetMailSerializer,
    RegisterSerializer,
    LogOutSerializer,
)


class OurTokenObtainPairViewSet(viewsets.ViewSet):
    serializer_class = OurTokenObtainPairSerializer


# for sending mail
def send_email(request):
    user_email = User.objects.get("email")
    send_mail("mail:", "asmitajha174@gmail.com", [user_email], fail_silently=False)
    return HttpResponse("Email has been sent!")


class RegisterViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            user = serializer.save()

            otp = OTP.objects.create(
                otp=(random.randint(100, 999)),
                user=user,
                created_at=datetime.datetime.now(),
                purpose="Registration",
            )

            otp.save()

            user.save()

            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)

            verification_url = f"http://localhost:8000/api/v1/verify_otp/"

            send_mail(
                "Registration Verfication",
                f'Click the link to verify your OTP ("One Time Password") for registration. {verification_url} . Your otp is {otp.otp}.',
                "asmitajha174@gmail.com",
                [user.email],
                fail_silently=False,
            )

            return Response(
                {
                    "message": f"Welcome to the Registration Process. Please verify your OTP (One Time Password) for successfully creating an account. Verify your otp through this link. {verification_url}"
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"message": "This user doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
#api for otp
@api_view(["POST"])
def otp_verification(request):
    serializer = OTPCheckSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    purpose = serializer.validated_data.get("purpose")
    otp = serializer.validated_data.get("otp")
    user = serializer.validated_data.get("user")

    otp_object = OTP.objects.filter(user=user, otp=otp).first()

    if not otp_object:
        return Response(
            {"message": "Invalid OTP. Try again."}, status=status.HTTP_400_BAD_REQUEST
        )
        
    if otp_object.otp_expired:
        return Response(
            {"message": "Your OTP has already expired. Please try again"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    refresh = RefreshToken.for_user(user)
    reset_token = str(refresh.access_token)
    

    if purpose == "password_change":
        reset_url = f"http://localhost:8000/api/v1/password-change/{reset_token}/"

        return Response(
            {
                "message": f"OTP verified successfully. you can successfully change your password through this link. {reset_url}."
            },
            status=status.HTTP_200_OK,
        )
    else:
            reset_url = f"http://localhost:8000/login/"
            return Response(
                {
                    "message": f"OTP verified successfully. Now, you can log in through this link: {reset_url}"
                },
                status=status.HTTP_200_OK,
            )

# api for login
@api_view(["POST"])
def user_login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    user = None

    if "@" in username:
        try:
            user = User.objects.get(email=username)
        except User.DoesNotExist:
            pass

    if not user:
        user = authenticate(username=username, password=password)

    if user:
        refresh = RefreshToken.for_user(user)

        return Response(
            {"refresh": str(refresh), "access": str(refresh.access_token)},
            status=status.HTTP_200_OK,
        )
    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_mail(request):
    serializer=PasswordResetMailSerializer(data=request.data)
    
    if serializer.is_valid():
        email=serializer.validated_data.get("email")
        
        user=User.objects.get(email=email)
            
        if user:
            refresh=RefreshToken.for_user(user)
            reset_token=str(refresh.access_token)
                
            #generating and saving the OTP instance
                
            otp=OTP.objects.create(
                otp=str(random.randint(100,999)),
                user=user,
                created_at=datetime.datetime.now(),
                )
            
            otp.save()
                
            verification_url=f"http://localhost:8000/api/v1/verify_otp/"
                
            send_mail(
                    "Password Reset",
                    f"Click the link to reset your password: {verification_url}",
                    "asmitajha174@gmail.com",
                    [user.email],
                    fail_silently=False,
                )
            
            return Response(
                    {
                        "message": f"Password reset request successful. Your OTP is {otp.otp}. Verify your OTP through this link: {verification_url}"
                    },
                    status=status.HTTP_200_OK,
                )
        else:
            return Response(
                {"message": "This user doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )
            
@api_view(["PATCH"])
@permission_classes([AllowAny])
def password_change(request,token):
    serializer=PasswordChangeSerializer(data=request.data, context={"token": token})
    
    if serializer.is_valid():
        user=serializer.validated_data["user"]
        user.set_password(serializer.validated_data["password"])
        user.save()
        
        send_mail(
            "Password Successfully Changed",
            "You can now log in to your account using your new password.",
            "asmitajha174@gmail.com",
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset completed successfully"},
            status=status.HTTP_200_OK,
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    
    
# for logout
class LogOutViewSet(viewsets.ViewSet):

    permission_classes = (IsAuthenticated,)
    serializer_class = LogOutSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            try:
                refresh_token = request.data["refresh"]
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response(
                    {
                        "message": "User with the given refresh token has been successfully logged out."
                    },
                    status=status.HTTP_205_RESET_CONTENT,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# for verification of OTP for registration as well as password change
"""class OTPVerificationViewSet(viewsets.ModelViewSet):
    queryset = OTP.objects.all()
    serializer_class = OTPCheckSerializer
    # permission_classes=[AllowAny,IsAuthenticated]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        purpose = serializer.validated_data.get("purpose")
        otp = serializer.validated_data["otp"]
        user = serializer.validated_data["user"]

        otp_instance = OTP.objects.filter(user=user, otp=otp).first()

        if not otp_instance:
            return Response(
                {"message": "Invalid OTP. Try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        otp_expired = otp_instance.otp_expired
        if otp_expired:
            return Response(
                {"message": "Your OTP has already been expired. Please try again."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        refresh = RefreshToken.for_user(user)
        reset_token = str(refresh.access_token)

        if purpose == "password_change":
            reset_url = f"http://localhost:8000/api/v1/password-change/{reset_token}/"
            return Response(
                {
                    "message": f"OTP verified successfully. Now, you can successfully change your password through this link. {reset_url}"
                },
                status=status.HTTP_200_OK,
            )

        else:
            reset_url = f"http://localhost:8000/login/"
            return Response(
                {
                    "message": f"OTP verified successfully. Now, you can login to your account through this link. {reset_url}"
                },
                status=status.HTTP_200_OK,
            )"""


'''class PasswordResetMailViewSet(viewsets.ViewSet):
    serializer_class = PasswordResetMailSerializer
    perimission_classes = [
        AllowAny,
    ]

    def create(self, request):
        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = User.objects.get(email=email)

        if user:
            refresh = RefreshToken.for_user(user)
            reset_token = str(refresh.access_token)

            # generating and saving the otp instance
            otp = OTP.objects.create(
                otp=str(random.randint(100, 999)),
                user=user,
                created_at=datetime.datetime.now(),
            )
            otp.save()

            verification_url = f"http://localhost:8000/api/v1/verify_otp/"

            send_mail(
                "Password Reset",
                f"Click the link to reset your password: {verification_url}",
                "asmitajha174@gmail.com",
                [user.email],
                fail_silently=False,
            )
            return Response(
                {
                    "message": f"Password reset request successful. Your otp is {otp.otp}. Verify your otp through this link. {verification_url}"
                },
                status=status.HTTP_200_OK,
            )

        else:
            return Response(
                {"message": "This user doesn't exist."},
                status=status.HTTP_400_BAD_REQUEST,
            )'''


'''class PasswordChangeViewSet(viewsets.ViewSet):
    serializer_class = PasswordChangeSerializer

    @action(detail=False, methods=["patch"], url_path="change-password")
    def change_password(self, request, token):
        serializer = self.get_serializer(data=request.data, context={"token": token})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        user.set_password(serializer.validated_data["password"])

        user.save()

        send_mail(
            "Password Successfully Changed. Now, you can login to your account through your new password.",
            "asmitajha174@gmail.com",
            [user.email],
            fail_silently=False,
        )

        return Response(
            {"message": "Password reset completed successfully"},
            status=status.HTTP_200_OK,
        )'''
