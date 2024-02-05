from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from users.api_views import UserSingUpViewSet, UserViewSet

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"signup", UserSingUpViewSet, basename="signup")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/auth/", include("djoser.urls.authtoken")),
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
