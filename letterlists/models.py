from django.db import models
from common.models import CommonModel


class Letterlist(CommonModel):
    letter = models.ManyToManyField(
        "letters.Letter",
        related_name="letterlist",
    )

    def __str__(self) -> str:
        return f"{self.letter}"
