from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return f"{self.name}"
