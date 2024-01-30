from rest_framework import serializers

from .models import User


class UserRetrieveSerializer(serializers.ModelSerializer):
    """
    Сериализатор просмотра пользователя
    """

    class Meta:
        model = User


class UserSignupSerializer(serializers.ModelSerializer):
    """
    Сериализатор регистрации пользователя
    """

    class Meta:
        model = User
        fields = ("email", "username", "first_name", "last_name", "sex", "birth_date")
