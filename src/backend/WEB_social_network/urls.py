from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("users.urls")),
    path("api/", include("communities.urls")),
    path("api/", include("posts.urls")),
    path("api/", include("chat.urls")),
]
