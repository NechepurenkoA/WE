from rest_framework import mixins, viewsets

from .models import Post
from .permissions import IsAuthenticatedOrAdminForPosts
from .serializers import PostSerializer


class PostsViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """Вью-сет модели 'Posts'."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticatedOrAdminForPosts,)
