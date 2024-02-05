from django.contrib.auth import password_validation
from rest_framework import serializers

from .models import Friendship, User


class UserRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели 'User'.
    """

    are_friends = serializers.SerializerMethodField(
        read_only=True,
        source="get_are_friends",
    )

    class Meta:
        model = User
        fields = (
            "avatar",
            "username",
            "first_name",
            "last_name",
            "sex",
            "age",
            "biography",
            "are_friends",
        )

    # WIP
    def get_are_friends(self, obj):
        request = self.context["request"]
        return Friendship.objects.filter(
            current_user_id=request.user.id,
            users=obj.id,
        ).exists()


class UserSignUpSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "sex",
            "age",
            "birth_date",
            "biography",
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "age": {"read_only": True},
        }

    def validate_password(self, data):
        password_validation.validate_password(data)
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
