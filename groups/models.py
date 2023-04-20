from django.db import models
from common.models import CommonModel
from categories.models import Category
from django.db.models import Count, Case, When, Q


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

    @property
    def stand_by_members_count(self):
        return (
            self.accessinfo.annotate(
                is_stand_by=Case(
                    When(is_signup=False, then=True),
                    default=False,
                    output_field=models.BooleanField(),
                ),
            ).aggregate(count=Count("is_stand_by", filter=Q(is_stand_by=True)))["count"]
            or 0
        )

    # @property
    # def stand_by_members_count(self):
    # return self.accessinfo.filter(is_signup=False).count()

    def __str__(self) -> str:
        return f"{self.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.categories.exists():
            Category.objects.create(name="전체글", group=self)
            Category.objects.create(name="인기글", group=self)
