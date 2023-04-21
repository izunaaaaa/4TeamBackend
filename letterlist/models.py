from django.db import models
from common.models import CommonModel


class Letterlist(CommonModel):
    user = models.ManyToManyField(
        "users.User",
        related_name="letterlist",
    )

    def __str__(self) -> str:
        return str(self.pk) + "'st "

    def users_list(self):
        return ", ".join([f"{user} / {user.pk}" for user in self.user.all()])


class Letter(CommonModel):
    sender = models.ForeignKey(
        "users.User",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="letter",
    )
    room = models.ForeignKey(
        "letterlist.Letterlist",
        on_delete=models.CASCADE,
        related_name="letter",
    )
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"
