from django.db import models
from common.models import CommonModel


class Category(CommonModel):
    name = models.CharField(max_length=100)
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="categories",
    )

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "categories"
        constraints = [
            models.UniqueConstraint(
                fields=["name", "group"],
                name="unique_category_name_group",
            )
        ]

    # def add_default_data():
    #     Category.objects.get_or_create(name='전체글')

    # def save(self):
    #     if not self.name:
    #         self.name = "전체글"
    #     super().save()

    # def save(self, *args, **kwargs):
    #     is_new_group = not bool(self.pk)  # check if the group is being created
    #     super().save(*args, **kwargs)
    #     if is_new_group:
    #         Category.objects.create(name="전체글", group=self)
