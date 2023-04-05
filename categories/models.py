from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    name = models.CharField(max_length=100)
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
    )
