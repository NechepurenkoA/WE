from rest_framework import permissions


class IsAuthenticatedOrAdminForPosts(permissions.IsAuthenticated):
    """Доступ к постам."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_superuser
            or obj.author.id == request.user.id
        )
