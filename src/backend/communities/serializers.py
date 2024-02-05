from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Community


class CommunitySerializer(serializers.ModelSerializer):

    followers_amount = serializers.IntegerField(
        source="get_followers_amount",
        read_only=True,
    )

    class Meta:
        model = Community
        fields = [
            "title",
            "slug",
            "creator",
            "description",
            "avatar",
            "followers_amount",
        ]
        extra_kwargs = {
            "creator": {
                "read_only": True,
            },
        }

    def create(self, validated_data):
        community = Community.objects.create(
            **validated_data, creator=self.context["request"].user
        )
        community.followers.add(self.context["request"].user)
        community.save()
        return community


class CommunityFollowSerializer(serializers.Serializer):

    def validate(self, data):
        request = self.context["request"]
        community_slug = self.context["view"].kwargs["slug"]
        creator = get_object_or_404(
            Community,
            slug=community_slug,
        ).creator
        user = request.user
        if request.method == "POST":
            if Community.objects.filter(
                followers=user,
                slug=community_slug,
            ).exists():
                raise ValidationError({"error": "Вы уже подписаны на это сообщество!"})
        if request.method == "DELETE":
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
