from django.db import models
from common.models import CommonModel


class Chatroom(CommonModel):
    user = models.ManyToManyField(
        "users.User",
        related_name="chatroom",
    )

    def __str__(self) -> str:
        return str(self.pk) + "'st "


class Message(CommonModel):
    sender = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="send_messages",
    )
    room = models.ForeignKey(
        "chats.Chatroom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"
