from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import IsAuthenticatedOrAdmin
from .serializers import UserRetrieveSerializer, UserSignUpSerializer


class UserSingUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин вью-сет для регистрации.
    """

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = [
        permissions.AllowAny,
    ]


class UserViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.UpdateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин вью-сет для объектов 'User'.
    """

    queryset = User.objects.all()
    serializer_class = UserRetrieveSerializer
    permission_classes = [
        IsAuthenticatedOrAdmin,
    ]
    lookup_field = "username"

    @action(
        methods=["get"],
        detail=False,
        url_path="me",
        serializer_class=UserRetrieveSerializer,
    )
    def users_own_profile(self, request):
        """Просмотр своего профиля."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # WIP
    @action(
        methods=["post"],
        detail=True,
        lookup_field="username",
        url_path="send_friend_request",
    )
    def send_friend_request(self, request, username): ...
