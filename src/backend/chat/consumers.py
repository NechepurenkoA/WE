import json
from http import HTTPStatus

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from chat.models import Chat, Message
from chat.serializers import MessageSerializer


class ChatConsumer(WebsocketConsumer):

    def connect(self):
        self.room_id = self.scope["url_route"]["kwargs"]["room_id"]
        self.room_group_name = f"chat_{self.room_id}"
        chat = Chat.objects.get(pk=self.room_id)
        user = self.scope["user"]

        if user != chat.receiver and user != chat.initiator:
            self.close(HTTPStatus.FORBIDDEN)
        else:
            async_to_sync(self.channel_layer.group_add)(
                self.room_group_name, self.channel_name
            )
            self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name, self.channel_name
        )

    def receive(self, text_data, bytes_data=None):
        text_data_json = json.loads(text_data)
        return_dict = {"type": "chat_message", "text": text_data_json["message"]}
        conversation = Chat.objects.get(pk=self.scope["url_route"]["kwargs"]["room_id"])
        sender = self.scope["user"]
        _message = Message.objects.create(
            sender=sender,
            text=return_dict["text"],
            conversation_id=conversation.id,
        )
        return_dict["sender"] = _message.sender.username
        return_dict["message_id"] = _message.pk

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            return_dict,
        )

    def chat_message(self, event):
        message = Message.objects.get(pk=event["message_id"])
        serializer = MessageSerializer(instance=message)
        self.send(text_data=json.dumps(serializer.data))
