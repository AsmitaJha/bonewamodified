from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from user.urls import router as user_router
from content.urls import router as content_router
from genre.urls import router as genre_router

router = DefaultRouter()

# router.registry.extend(user_router.registry)
# router.registry.extend(content_router.registry)
# router.registry.extend(genre_router.registry)


urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("admin/", admin.site.urls),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("", include("user.urls")),
    path("", include("content.urls")),
    path("", include("genre.urls")),
    path("", include("genre.urls")),
]
