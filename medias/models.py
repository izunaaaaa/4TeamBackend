from django.db import models
from common.models import CommonModel


class Image(CommonModel):
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="images",
    )
    url = models.URLField()
