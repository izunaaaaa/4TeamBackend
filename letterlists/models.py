from django.db import models
from common.models import CommonModel


class Letterlist(CommonModel):
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="letterlist",
    )
    receiver = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="letterlist",
    )

    def __str__(self) -> str:
        return f"To {self.sender} from {self.receiver}"
