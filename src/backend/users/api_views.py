from http import HTTPMethod

from django.forms import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import User
from .permissions import IsAuthenticatedOrAdminForUsers
from .serializers import (
    FriendRequestSerializer,
    UserRetrieveSerializer,
    UserSignUpSerializer,
)
from .services import FriendRequestServices


class UserSingUpViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    Миксин вью-сет для регистрации.
    """

    queryset = User.objects.all()
    serializer_class = UserSignUpSerializer
    permission_classes = (permissions.AllowAny,)


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
    permission_classes = (IsAuthenticatedOrAdminForUsers,)
    lookup_field = "username"

    def get_friend_request_serializer(self, *args, **kwargs):
        serializer_class = FriendRequestSerializer
        kwargs.setdefault("context", self.get_serializer_context())
        return serializer_class(*args, **kwargs)

    @action(
        methods=[HTTPMethod.GET],
        detail=False,
        url_path="me",
    )
    def users_own_profile(self, request):
        """Просмотр своего профиля."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        methods=[HTTPMethod.POST, HTTPMethod.DELETE],
        detail=True,
        lookup_field="username",
        url_path="send_friend_request",
    )
    def send_friend_request(self, request, username):
        """Отправление запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_friend_request_serializer(data=model_to_dict(user))
        serializer.is_valid(raise_exception=True)
        if request.method == HTTPMethod.POST:
            FriendRequestServices(request).send_friend_request(user=user)
            return Response(
                {"message": f"Вы отправили запрос дружбы пользователю {username}!"},
                status=status.HTTP_201_CREATED,
            )
        if request.method == HTTPMethod.DELETE:
            FriendRequestServices(request).cancel_friend_request(user=user)
            return Response(
                {"message": f"Вы отозвали запрос дружбы к пользователю {username}!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    # WIP
    @action(
        methods=["post"],
        detail=True,
        lookup_field="username",
        url_path="accept_friend_request",
    )
    def accept_friend_request(self, request, username):
        """Принятие запроса дружбы."""
        ...

    # WIP
    @action(
        methods=[HTTPMethod.DELETE],
        detail=True,
        lookup_field="username",
        url_path="decline_friend_request",
    )
    def decline_friend_request(self, request, username):
        """Отклонение запроса дружбы."""
        ...


class FriendshipViewSet(
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = UserRetrieveSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def get_queryset(self):
        query = self.request.user.friends.all()
        return query
