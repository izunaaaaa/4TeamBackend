from django.db import models
from common.models import CommonModel
from django.core.exceptions import ValidationError


class Feedlike(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    feed = models.ForeignKey(
        "feeds.Feed",
        on_delete=models.CASCADE,
        related_name="feedlike",
    )
    unique_together = ("user", "feed")


class Commentlike(CommonModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
    )
    comment = models.ForeignKey(
        "comments.Comment",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name="commentlike",
    )
    recomment = models.ForeignKey(
        "comments.Recomment",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="recommentlike",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_like",
            ),
            models.UniqueConstraint(
                fields=["user", "recomment"],
                name="unique_recomment_like",
            ),
        ]

    def clean(self):
        if self.comment and self.recomment:
            raise ValidationError(
                "Cannot like both a comment and a recomment in the same instance."
            )
        if not self.comment and not self.recomment:
            raise ValidationError("Must like either a comment or a recomment.")
