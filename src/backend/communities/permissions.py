from rest_framework import permissions


class IsAuthenticatedOrAdminForCommunities(permissions.IsAuthenticated):
    """Доступ к сообществам."""

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser or obj.creator == request.user
