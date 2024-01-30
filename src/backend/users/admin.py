from django.contrib import admin

from .models import User


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
    list_filter = (
        "username",
        "is_staff",
        "is_superuser",
    )
    empty_value_display = "-пусто-"
