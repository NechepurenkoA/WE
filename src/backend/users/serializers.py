from http import HTTPMethod

from django.contrib.auth import password_validation
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users.models import FriendRequest, User


class UserRetrieveSerializer(serializers.ModelSerializer):
    """Сериализатор модели 'User'."""

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
            "gender",
            "age",
            "biography",
            "are_friends",
        )

    # WIP
    def get_are_friends(self, obj):
        user = self.context["request"].user
        return user.friends.filter(id=obj.id).exists()


class UserSignUpSerializer(serializers.ModelSerializer):
    """Сериализатор для регистрации пользователей."""

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "gender",
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


class FriendRequestSerializer(serializers.Serializer):
    """Сериализатор для запроса дружбы."""

    username = serializers.SlugField()

    def validate(self, data):
        request = self.context["request"]
        username = data["username"]
        user = get_object_or_404(User, username=username)
        if user == request.user:
            raise ValidationError(
                {"error": "Нельзя проводить подобные операции с самим собой!"}
            )
        if request.method == HTTPMethod.POST:
            if FriendRequest.objects.filter(
                sender=user, receiver=request.user
            ).exists():
                raise ValidationError(
                    {"error": f"Вы уже друзья с пользователем {username}!"}
                )
            if FriendRequest.objects.filter(
                sender=user, receiver=request.user
            ).exists():
                raise ValidationError(
                    {
                        "error": f"Пользователь {username} уже отправил"
                        f" вам запрос дружбы!"
                    }
                )
            if FriendRequest.objects.filter(
                sender=request.user, receiver=user
            ).exists():
                raise ValidationError(
                    {
                        "error": f"Вы уже отправили запрос"
                        f" дружбы пользователю {username}!"
                    }
                )
        if request.method == HTTPMethod.DELETE:
            if not FriendRequest.objects.filter(
                sender=request.user, receiver=user
            ).exists():
                raise ValidationError(
                    {
                        "error": f"Вы не отправляли запрос"
                        f" дружбы пользователю {username}!"
                    }
                )
        return data


class FriendAcceptDeclineSerializer(serializers.Serializer):
    """Сериализатор accept / decline запроса дружбы."""

    username = serializers.SlugField()

    def validate(self, data):
        request = self.context["request"]
        username = data["username"]
        user = get_object_or_404(User, username=username)
        if user == request.user:
            raise ValidationError(
                {"error": "Нельзя проводить подобные операции с самим собой!"}
            )
        if request.method == HTTPMethod.POST:
            if not FriendRequest.objects.filter(
                receiver=request.user, sender=user
            ).exists():
                raise ValidationError(
                    {"error": "Этот пользователь не отправлял вам запрос дружбы!"}
                )
        if request.method == HTTPMethod.DELETE:
            if not FriendRequest.objects.filter(
                receiver=request.user, sender=user
            ).exists():
                raise ValidationError(
                    {"error": "Этот пользователь не отправлял вам запрос дружбы!"}
                )
        return data


class ChangePasswordSerializer(serializers.Serializer):
    """
    Сериализатор смены пароля.
    """

    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)

    def validate_old_password(self, data):
        request = self.context["request"]
        if request.user.check_password(data):
            return data
        raise ValidationError("Старый пароль не совпадает!")
