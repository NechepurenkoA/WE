from django.db import models

from users.models import User


class Chat(models.Model):
    """Модель чата."""

    initiator = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_starter"
    )
    receiver = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="convo_participant"
    )
    start_time = models.DateTimeField(auto_now_add=True)


class Message(models.Model):
    """Модель сообщения в чате."""

    sender = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="message_sender",
    )
    text = models.TextField(
        blank=True,
    )
    attachment = models.FileField(
        blank=True,
    )
    conversation = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        ordering = ("-timestamp",)
