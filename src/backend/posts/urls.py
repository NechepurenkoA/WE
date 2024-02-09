from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .api_views import PostsViewSet

router = DefaultRouter()
router.register(r"feed", PostsViewSet, basename="posts")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
