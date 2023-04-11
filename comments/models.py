from django.db import models
from common.models import CommonModel


class Comment(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="comment",
    )
    description = models.TextField(
        max_length=255,
    )
 
    def __str__(self) -> str:
        return f"{self.description}"
    
    @property
    def top_comment_like(self):
        if self.media.all().count() > 0:
            return self.media.all()[0]
        else:
            return ""