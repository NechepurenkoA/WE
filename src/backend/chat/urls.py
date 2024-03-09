from django.conf import settings
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"", ..., basename="chat")

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/", include(router.urls)),
]
