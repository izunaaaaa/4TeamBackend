from django.db import models
from common.models import CommonModel


class Group(CommonModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self) -> str:
        return f"{self.name}"
