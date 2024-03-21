from http import HTTPMethod

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from communities.models import Community


class CommunitySerializer(serializers.ModelSerializer):
    """Сериализатор модели 'Community'."""

    followers_amount = serializers.IntegerField(
        source="get_followers_amount",
        read_only=True,
    )
    is_followed = serializers.SerializerMethodField(
        source="get_is_followed",
        read_only=True,
    )

    class Meta:
        model = Community
        fields = [
            "id",
            "avatar",
            "title",
            "slug",
            "creator",
            "description",
            "is_followed",
            "followers_amount",
        ]
        extra_kwargs = {
            "creator": {
                "read_only": True,
            },
            "id": {
                "read_only": True,
            },
        }

    def get_is_followed(self, obj) -> bool:
        user = self.context["request"].user
        return Community.objects.filter(followers__id=user.id, id=obj.id).exists()

    def create(self, validated_data):
        community = Community.objects.create(
            **validated_data, creator=self.context["request"].user
        )
        community.followers.add(self.context["request"].user)
        community.save()
        return community


class CommunityFollowSerializer(serializers.Serializer):
    """Сериализатор подписывания на сообщество."""

    slug = serializers.SlugField()

    def validate(self, data):
        request = self.context["request"]
        community_slug = data["slug"]
        creator = get_object_or_404(
            Community,
            slug=community_slug,
        ).creator
        user = request.user
        if request.method == HTTPMethod.POST:
            if Community.objects.filter(
                followers=user,
                slug=community_slug,
            ).exists():
                raise ValidationError({"error": "Вы уже подписаны на это сообщество!"})
        if request.method == HTTPMethod.DELETE:
            if creator == user:
                raise ValidationError(
                    {"error": "Нельзя отписаться от созданного вами сообщества!"}
                )
            if not Community.objects.filter(
                followers=user,
                slug=community_slug,
            ).exists():
                raise ValidationError({"error": "Вы не подписаны на это сообщество!"})
        return data
