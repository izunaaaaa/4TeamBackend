from django.db import models
from common.models import CommonModel
from categories.models import Category


class Group(CommonModel):
    name = models.CharField(max_length=100, unique=True)
    # coach = models.OneToOneField(
    #     "users.User",
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name="coaching_group",
    #     # # related_name="group",
    # )
    description = models.TextField(blank=True)

    @property
    def members_count(self):
        return self.members.count()

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.categories.exists():
            Category.objects.create(name="전체글", group=self)
            Category.objects.create(name="인기글", group=self)
