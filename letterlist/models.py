from django.db import models
from common.models import CommonModel
from django.core.exceptions import ValidationError


class Letterlist(CommonModel):
    user = models.ManyToManyField(
        "users.User",
        related_name="letterlist",
    )

    ignore_by = models.ManyToManyField(
        "users.User",
        related_name="deleted_letter_list",
        blank=True,
    )

    @property
    def ignore_user(self):
        if self.ignore_by.exists():
            return "".join([i.username for i in self.ignore_by.all()])
        else:
            return None

    def __str__(self) -> str:
        return str(self.pk) + "'st "

    def users_list(self):
        return ", ".join([f"{user} / {user.pk} " for user in self.user.all()])

    @property
    def letter_count(self):
        return self.letter.count()

    @property
    def last_letter(self):
        if self.letter.exists():
            return self.letter.order_by("-created_at").first().text
        else:
            return "메세지가 없습니다."


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

    delete_by = models.ManyToManyField(
        "users.User",
        related_name="deleted_letters",
        blank=True,
    )

    def __str__(self):
        return f"{self.text}"

    @property
    def delete_user(self):
        if self.delete_by.exists():
            return "".join([i.username for i in self.delete_by.all()])
        else:
            return None
