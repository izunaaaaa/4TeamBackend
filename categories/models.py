from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "categories"
