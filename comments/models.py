from django.db import models
from common.models import CommonModel


class Comment(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
    )
    description = models.TextField(
        max_length=255,
    )

    def __str__(self) -> str:
        return f"{self.feed}"
