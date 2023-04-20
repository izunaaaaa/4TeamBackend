from django.db import models
from common.models import CommonModel


class Chattingroom(CommonModel):
    user = models.ManyToManyField(
        "users.User",
        related_name="chatroom",
    )

    def __str__(self) -> str:
        return str(self.pk) + "'st "

    def users_list(self):
        return ", ".join([f"{user} / {user.pk}" for user in self.user.all()])


class Message(CommonModel):
    sender = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="send_messages",
    )
    room = models.ForeignKey(
        "chattings.Chattingroom",
        on_delete=models.CASCADE,
        related_name="messages",
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"
