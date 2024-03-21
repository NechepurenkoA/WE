from http import HTTPStatus

from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from chat.models import Chat, Message
from users.models import Friendship, User


class UsernameForChatSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["username"]


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = [
            "sender",
            "text",
            "timestamp",
        ]


class ChatAbstractSerializer(serializers.ModelSerializer):
    initiator = UsernameForChatSerializer()
    receiver = UsernameForChatSerializer()


class ChatSerializer(ChatAbstractSerializer):
    messages = serializers.SerializerMethodField(method_name="get_messages")

    class Meta:
        model = Chat
        fields = [
            "id",
            "initiator",
            "receiver",
            "messages",
        ]

    def get_messages(self, instance):
        serializer = MessageSerializer(instance=instance.messages, many=True)
        return serializer.data


class ChatListSerializer(ChatAbstractSerializer):
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = Chat
        fields = [
            "id",
            "initiator",
            "receiver",
            "last_message",
        ]

    def get_last_message(self, instance):
        message = instance.messages.first()
        return MessageSerializer(instance=message).data


class ChatCreateSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        request = self.context["request"]
        receiver = get_object_or_404(User, username=data["username"])
        friendship = Friendship.objects.filter(
            current_user_id=request.user.id,
            another_user_id=receiver.id,
        )
        if not friendship.exists():
            raise ValidationError(
                {"message": "Для общения нужно быть друзьями!"}, HTTPStatus.FORBIDDEN
            )
        return data
