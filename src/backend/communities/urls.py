from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from communities.api_views import CommunityViewSet

router = DefaultRouter()
router.register(r"communities", CommunityViewSet, basename="communities")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
