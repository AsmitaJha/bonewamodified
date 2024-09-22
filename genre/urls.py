from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api import *

router = DefaultRouter()
router.register("genre", GenreViewSet, basename="genre")

#urlpatterns = [path("", include(router.urls))]

urlpatterns=[
    path("api/v1/",include(router.urls))
]
