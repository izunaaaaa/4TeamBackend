from django.db import models
from common.models import CommonModel


class Letter(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    description = models.CharField(max_length=100)
