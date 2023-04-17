from django.db import models
from common.models import CommonModel


class Letterlist(CommonModel):
    letter = models.ForeignKey(
        "letters.Letter",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self) -> str:
        return f"{self.letter}"
