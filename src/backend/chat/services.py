from django.shortcuts import get_object_or_404
from rest_framework.request import Request

from chat.models import Chat
from users.models import User


class ChatServices(object):

    def __init__(self, request: Request):
        self.request = request

    def start_chat(self, receiver_id: int) -> Chat:
        initiator = self.request.user
        receiver = get_object_or_404(User, pk=receiver_id)
        chat = Chat.objects.create(initiator=initiator, receiver=receiver)
        return chat
