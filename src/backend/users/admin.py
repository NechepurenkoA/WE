from django.contrib import admin

from users.models import FriendRequest, Friendship, User


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


@admin.register(Friendship)
class Friendship(admin.ModelAdmin):
    """Админка дружбы."""

    search_fields = ("username",)
    list_filter = (
        "current_user",
        "friends_from",
    )
    empty_value_display = "-пусто-"


@admin.register(FriendRequest)
class FriendRequest(admin.ModelAdmin):
    """Админка запроса дружбы."""

    list_display = ("sender", "receiver")
    search_fields = ("username",)
    list_filter = (
        "sender",
        "receiver",
        "sent_on",
    )
    empty_value_display = "-пусто-"
