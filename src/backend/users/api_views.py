from http import HTTPMethod

from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import Friendship, User
from users.permissions import IsAuthenticatedOrAdminForUsers
from users.serializers import (
    ChangePasswordSerializer,
    FriendAcceptDeclineSerializer,
    FriendRequestSerializer,
    UserRetrieveSerializer,
    UserSignUpSerializer,
)
from users.services import FriendRequestServices, FriendshipServices, UserServices


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
        serializer_class=FriendRequestSerializer,
    )
    def send_friend_request(self, request, username):
        """Отправление запроса дружбы."""
        serializer = self.get_serializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        if request.method == HTTPMethod.POST:
            user = get_object_or_404(User, username=username)
            FriendRequestServices(request).send_friend_request(user=user)
            return Response(
                {"message": f"Вы отправили запрос дружбы пользователю {username}!"},
                status=status.HTTP_201_CREATED,
            )
        if request.method == HTTPMethod.DELETE:
            user = get_object_or_404(User, username=username)
            FriendRequestServices(request).cancel_friend_request(user=user)
            return Response(
                {"message": f"Вы отозвали запрос дружбы к пользователю {username}!"},
                status=status.HTTP_204_NO_CONTENT,
            )

    @action(
        methods=[HTTPMethod.POST],
        detail=True,
        lookup_field="username",
        url_path="accept_friend_request",
        serializer_class=FriendAcceptDeclineSerializer,
    )
    def accept_friend_request(self, request, username):
        """Принятие запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(
            data={"username": username}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        FriendRequestServices(request).accept_friend_request(user)
        return Response(
            {"message": f"Вы приняли запрос дружбы от пользователя {username}!"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=[HTTPMethod.DELETE],
        detail=True,
        lookup_field="username",
        url_path="decline_friend_request",
        serializer_class=FriendAcceptDeclineSerializer,
    )
    def decline_friend_request(self, request, username):
        """Отклонение запроса дружбы."""
        user = get_object_or_404(User, username=username)
        serializer = self.get_serializer(
            data={"username": username}, context=self.get_serializer_context()
        )
        serializer.is_valid(raise_exception=True)
        FriendRequestServices(request).decline_friend_request(user)
        return Response(
            {"message": f"Вы отклонили запрос дружбы от пользователя {username}!"},
            status=status.HTTP_201_CREATED,
        )


class FriendshipViewSet(
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    """Вьюсет для списка друзей."""

    serializer_class = UserRetrieveSerializer
    permission_classes = [
        permissions.IsAuthenticated,
    ]
    lookup_field = "username"

    def get_queryset(self):
        """Запрос, возвращающий друзей пользователя."""
        query = self.request.user.friends_list
        return query

    def destroy(self, request, *args, **kwargs):
        """Удаление из друзей."""

        user_id: int = get_object_or_404(User, username=kwargs["username"]).id
        friendship = get_object_or_404(
            Friendship,
            another_user_id=user_id,
            current_user_id=request.user.id,
        )
        FriendshipServices(request).remove_friend(friendship)
        return Response(
            {"message": f"Вы удалили пользователя {kwargs['username']} из друзей!"},
            status=status.HTTP_204_NO_CONTENT,
        )


@api_view([HTTPMethod.POST])
@permission_classes([IsAuthenticated])
def change_password(request):
    """Смена пароля."""

    serializer = ChangePasswordSerializer(
        data=request.data, context={"request": request}
    )
    if serializer.is_valid():
        UserServices(request).change_password(serializer.validated_data["new_password"])
        return Response(
            {"message": "Пароль изменен успешно!"},
            status=status.HTTP_200_OK,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
