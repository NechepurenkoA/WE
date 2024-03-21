from http import HTTPMethod, HTTPStatus

from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from chat.models import Chat
from chat.serializers import ChatCreateSerializer, ChatListSerializer, ChatSerializer
from chat.services import ChatServices
from users.models import User


class ChatViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "username"

    def get_queryset(self):
        query = Chat.objects.filter(
            Q(initiator=self.request.user) | Q(receiver=self.request.user)
        )
        return query

    def list(self, request):
        list_of_chats = self.get_queryset()
        serializer = ChatListSerializer(instance=list_of_chats, many=True)
        return Response(serializer.data, HTTPStatus.OK)

    def retrieve(self, request, username: str):
        participant = get_object_or_404(User, username=username)
        if participant == request.user:
            return Response(
                {"error": "Нельзя проводить операции с самим собой!"},
                HTTPStatus.FORBIDDEN,
            )
        conversation = Chat.objects.filter(
            Q(initiator=request.user, receiver=participant)
            | Q(initiator=participant, receiver=request.user)
        )
        if not conversation.exists():
            return Response(
                {"error": "У вас нет активного чата с этим пользователем!"},
                HTTPStatus.NO_CONTENT,
            )
        serializer = ChatSerializer(instance=conversation.first())
        return Response(serializer.data, HTTPStatus.OK)

    @action(
        methods=[HTTPMethod.POST],
        url_path="start",
        detail=True,
        serializer_class=ChatCreateSerializer,
    )
    def start_chat(self, request, username):
        participant = get_object_or_404(User, username=username)
        serializer = self.get_serializer(data={"username": username})
        serializer.is_valid(raise_exception=True)
        chat = Chat.objects.filter(
            Q(initiator=request.user, receiver=participant)
            | Q(initiator=participant, receiver=request.user)
        )
        if chat.exists():
            return self.retrieve(request, username=username)
        chat = ChatServices(request).start_chat(participant.id)
        chat_serializer = ChatSerializer(
            instance=chat,
            context=self.get_serializer_context(),
        )
        return Response(chat_serializer.data, HTTPStatus.CREATED)
