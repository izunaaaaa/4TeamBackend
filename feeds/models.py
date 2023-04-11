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
    category = models.ForeignKey(
        "categories.Category",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    visited = models.PositiveIntegerField(
        editable=False,
        default=0,
    )
    

    def __str__(self) -> str:
        return f"{self.title}"

    @property
    def likeCount(self):
        return self.feedlike.count()
    
    @property
    def commentlikeCount(self):
        return self.commentlike.count()