from http import HTTPMethod

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Like, Post
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
            "communities",
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
            "communities": {
                "required": False,
            },
        }

    def get_likes_amount(self, obj):
        return obj.likes.count()

    def validate(self, attrs):
        if not bool(attrs):
            raise ValidationError("Нельзя передавать пустой JSON!")
        return super().validate(attrs)

    def validate_text(self, text):
        data = self.context["request"].data
        return validate_text_or_image(data, text, "image")

    def validate_image(self, image):
        data = self.context["request"].data
        return validate_text_or_image(data, image, "text")

    def create(self, validated_data):
        try:
            communities = validated_data.pop("communities")
            post = Post.objects.create(
                **validated_data, author=self.context["request"].user
            )
            post.communities.set(communities)
            post.save()
        except KeyError:
            post = Post.objects.create(
                **validated_data, author=self.context["request"].user
            )
            post.save()
        return post


class PostLikeSerialzier(serializers.Serializer):
    post_id = serializers.IntegerField()

    def validate(self, data):
        request = self.context["request"]
        user = request.user
        if request.method == HTTPMethod.POST:
            if Like.objects.filter(post_id=data["post_id"], user_id=user.id).exists():
                raise ValidationError(
                    {"error": "Вы уже поставили лайк под этим постом!"}
                )
        if request.method == HTTPMethod.DELETE:
            if not Like.objects.filter(
                post_id=data["post_id"], user_id=user.id
            ).exists():
                raise ValidationError({"error": "Вы не ставили лайк под этим постом!"})
        return data
