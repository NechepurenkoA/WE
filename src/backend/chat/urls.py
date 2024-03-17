from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from chat.api_views import ChatViewSet

router = DefaultRouter()
router.register(r"chats", ChatViewSet, basename="chats")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
