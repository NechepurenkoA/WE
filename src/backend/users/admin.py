from django.contrib import admin

from .models import Group, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админка пользователей."""

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "age",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("username",)
    list_filter = ("username", "is_staff", "is_superuser")
    empty_value_display = "-пусто-"


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админка группы."""

    list_display = (
        "title",
        "creator",
        "slug",
        "description",
    )
    search_fields = ("slug",)
    list_filter = ("slug",)
    empty_value_display = "-пусто-"
