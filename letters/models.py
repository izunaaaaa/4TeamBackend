from django.db import models
from common.models import CommonModel


class Letter(CommonModel):
    list = models.ForeignKey(
        "letterlists.Letterlist",
        on_delete=models.CASCADE,
        related_name="letter",
    )
    description = models.CharField(max_length=100)
