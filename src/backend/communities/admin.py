from django.contrib import admin

from .models import Community


@admin.register(Community)
class CommunityAdmin(admin.ModelAdmin):
    """Админка сообщества."""

    list_display = (
        "title",
        "creator",
        "slug",
        "description",
        "get_followers_amount",
    )
    search_fields = ("slug",)
    list_filter = ("slug",)
    empty_value_display = "-пусто-"
