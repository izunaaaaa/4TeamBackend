from django.db import models
from common.models import CommonModel


class Recomment(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
    )
    description = models.TextField()
