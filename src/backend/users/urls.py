from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.api_views import (
    FriendshipViewSet,
    UserSingUpViewSet,
    UserViewSet,
    change_password,
)

router = DefaultRouter()
router.register(r"users", UserViewSet, basename="users")
router.register(r"signup", UserSingUpViewSet, basename="signup")
router.register(r"friends", FriendshipViewSet, basename="friends")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/auth/", include("djoser.urls.authtoken")),
    path(
        f"{settings.API_V1_PREFIX}/",
        include(router.urls),
    ),
    path(
        f"{settings.API_V1_PREFIX}/change_password/",
        change_password,
        name="change_password",
    ),
    path(
        f"{settings.API_V1_PREFIX}/password_reset/",
        include(
            "django_rest_passwordreset.urls",
        ),
    ),
]
