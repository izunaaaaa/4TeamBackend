from django.db import models
from common.models import CommonModel


class Media(CommonModel):
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="media"
    )
    url = models.URLField()
