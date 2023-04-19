from django.db import models
from common.models import CommonModel


class Chattingroom(CommonModel):
    user = models.ManyToManyField(
        "users.User",
        related_name="chattingroom_users",
    )

    def __str__(self) -> str:
        return f"{self.pk}"


class Chat(CommonModel):
    chattingroom = models.ForeignKey(
        "chattings.Chattingroom",
        on_delete=models.CASCADE,
        related_name="chattingroom",
    )
    message = models.TextField()

    def __str__(self) -> str:
        return f"{self.pk}"
