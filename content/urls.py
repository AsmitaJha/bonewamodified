from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()

router.register(r"add-comment", AddCommentView, basename="add-comment")
router.register(r"create-content", ContentCreateView, basename="create-content")
urlpatterns = [
    path("api/v1/", include(router.urls)),
]
