from django.db import models
from common.models import CommonModel


class Letter(CommonModel):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="sender",
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="receiver",
    )
    description = models.CharField(max_length=100)
