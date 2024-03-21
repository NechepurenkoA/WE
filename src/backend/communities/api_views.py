from http import HTTPMethod, HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from communities.models import Community
from communities.permissions import IsAuthenticatedOrAdminForCommunities
from communities.serializers import CommunityFollowSerializer, CommunitySerializer
from communities.services import FollowService
from users.serializers import UserRetrieveSerializer


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
        methods=[HTTPMethod.GET],
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
            status=HTTPStatus.OK,
        )

    @action(
        methods=[HTTPMethod.POST],
        detail=True,
        url_path="follow",
        lookup_field="slug",
        serializer_class=CommunityFollowSerializer,
    )
    def community_follow(self, request, slug):
        """Подписка на сообщество."""
        serializer = self.get_serializer(data={"slug": slug})
        serializer.is_valid(raise_exception=True)
        community = get_object_or_404(Community, slug=slug)
        FollowService(request).add_follower(community)
        return Response(
            {"message": f"Вы подписались на сообщество {community.title}!"},
            status=HTTPStatus.CREATED,
        )

    @action(
        methods=[HTTPMethod.DELETE],
        detail=True,
        url_path="unfollow",
        lookup_field="slug",
        serializer_class=CommunityFollowSerializer,
    )
    def community_unfollow(self, request, slug):
        """Отписка от сообщества."""
        serializer = self.get_serializer(data={"slug": slug})
        serializer.is_valid(raise_exception=True)
        community = get_object_or_404(Community, slug=slug)
        FollowService(request).remove_follower(community)
        return Response(
            status=HTTPStatus.NO_CONTENT,
        )
