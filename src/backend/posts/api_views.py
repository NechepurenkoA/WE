from http import HTTPMethod, HTTPStatus

import django_filters.rest_framework
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from posts.models import Post
from posts.permissions import IsAuthenticatedOrAdminForPosts
from posts.serializers import PostLikeSerialzier, PostSerializer
from posts.services import PostServices


class PostsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Вью-сет модели 'Posts'."""

    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrAdminForPosts,)
    filter_backends = (
        django_filters.rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
    )
    filterset_fields = [
        "author",
        "communities",
    ]
    search_fields = [
        "author__username",
        "communities__slug",
        "text",
    ]

    def get_queryset(self):
        user = self.request.user
        if user.friends_list.count() == 0 and user.communities.count() == 0:
            return Post.objects.all()
        communities = user.communities.values_list("id", flat=True)
        friend_list = user.friends_list.values_list("id", flat=True)
        query_friends = Post.objects.filter(author_id__in=friend_list)
        query_communities = Post.objects.filter(communities__in=communities)
        query_user = Post.objects.filter(author_id=user.id)
        query = (query_friends | query_communities | query_user).distinct()
        return query

    @action(
        methods=[HTTPMethod.POST, HTTPMethod.DELETE],
        detail=True,
        url_path="like",
    )
    def like_post(self, request, pk):
        """Лайкнуть / анлайкнуть пост."""
        serializer = PostLikeSerialzier(
            context={"request": request}, data={"post_id": pk}
        )
        serializer.is_valid(raise_exception=True)
        if request.method == HTTPMethod.POST:
            post = get_object_or_404(Post, pk=pk)
            PostServices(request).like_post(post)
            return Response(
                {
                    "message": "Вы лайкнули пост!",
                    "post": self.get_serializer(post).data,
                },
                HTTPStatus.CREATED,
            )
        if request.method == HTTPMethod.DELETE:
            post = get_object_or_404(Post, pk=pk)
            PostServices(request).unlike_post(post)
            return Response(
                {
                    "message": "Вы убрали лайк с поста!",
                    "post": self.get_serializer(post).data,
                },
                HTTPStatus.OK,
            )
        return Response(serializer.errors, HTTPStatus.BAD_REQUEST)
