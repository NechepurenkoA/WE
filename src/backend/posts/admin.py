from django.contrib import admin

from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """Админка постов."""

    list_display = (
        "author",
        "publish_date",
        "text",
    )
    search_fields = (
        "author",
        "text",
    )
    list_filter = (
        "author",
        "publish_date",
    )
    empty_value_display = "-пусто-"
