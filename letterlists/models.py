from django.db import models
from common.models import CommonModel


class Letterlist(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    message = models.ManyToManyField("letters.Letter")
