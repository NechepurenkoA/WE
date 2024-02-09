from rest_framework import serializers

from .models import Post
from .services import validate_text_or_image


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор модели 'Post'."""

    author = serializers.SlugRelatedField(
        slug_field="username",
        read_only=True,
    )
    likes_amount = serializers.SerializerMethodField(
        source="get_likes_amount",
    )

    class Meta:
        model = Post
        fields = [
            "id",
            "author",
            "publish_date",
            "text",
            "image",
            "likes",
            "likes_amount",
        ]
        extra_kwargs = {
            "likes_amount": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
        }

    def get_likes_amount(self, obj):
        return obj.likes.count()

    def validate_text(self, text):
        data = self.context["request"].data
        return validate_text_or_image(data, text, "image")

    def validate_image(self, image):
        data = self.context["request"].data
        return validate_text_or_image(data, image, "text")

    def create(self, validated_data):
        post = Post.objects.create(
            **validated_data, author=self.context["request"].user
        )
        post.save()
        return post
