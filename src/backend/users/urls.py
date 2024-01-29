from django.conf import settings
from django.urls import include, path

urlpatterns = [
    path(f"{settings.API_V1_PREFIX}/auth/", include("djoser.urls.authtoken")),
]
