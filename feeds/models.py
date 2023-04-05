from django.db import models
from common.models import CommonModel


class Feed(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )
