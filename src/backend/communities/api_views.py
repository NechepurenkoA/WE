from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from users.serializers import UserRetrieveSerializer

from .models import Community
from .permissions import IsAuthenticatedOrAdminForCommunities
from .serializers import CommunityFollowSerializer, CommunitySerializer
from .services import FollowService


class CommunityViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer
    lookup_field = "slug"
    permission_classes = (IsAuthenticatedOrAdminForCommunities,)

    @action(
        methods=["get"],
        detail=True,
        url_path="followers",
        lookup_field="slug",
        serializer_class=UserRetrieveSerializer,
    )
    def community_followers(self, request, slug):
        """Возвращает всех подписчиков сообщества."""
        community = get_object_or_404(Community, slug=slug)
        serializer = self.get_serializer(
            community.followers.all(),
            many=True,
        )
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @action(
        methods=["post"],
        detail=True,
        url_path="follow",
        lookup_field="slug",
        serializer_class=CommunityFollowSerializer,
    )
    def community_follow(self, request, slug):
        """Подписка на сообщество."""
        community = get_object_or_404(Community, slug=slug)
        serializer = self.get_serializer(data=model_to_dict(community))
        serializer.is_valid(raise_exception=True)
        FollowService(request).add_follower(community)
        return Response(
            {"message": f"Вы подписались на сообщество {community.title}!"},
            status=status.HTTP_201_CREATED,
        )

    @action(
        methods=["delete"],
        detail=True,
        url_path="unfollow",
        lookup_field="slug",
        serializer_class=CommunityFollowSerializer,
    )
    def community_unfollow(self, request, slug):
        """Отписка от сообщества."""
        community = get_object_or_404(Community, slug=slug)
        serializer = self.get_serializer(data=model_to_dict(community))
        serializer.is_valid(raise_exception=True)
        FollowService(request).remove_follower(community)
        return Response(
            {"message": f"Вы отписались от сообщества {community.title}!"},
            status=status.HTTP_204_NO_CONTENT,
        )

    # WIP
    @action(
        methods=["get"],
        detail=True,
        url_path="posts",
        lookup_field="slug",
        serializer_class=...,
    )
    def community_posts(self, request, slug):
        """Просмотр постов сообщества."""
        ...
