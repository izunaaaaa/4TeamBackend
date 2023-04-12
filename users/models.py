from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class GenderChoices(models.TextChoices):
        MALE = ("male", "Male")
        FEMALE = ("female", "Female")

    avatar = models.URLField(
        blank=True,
        null=True,
    )
    name = models.CharField(
        max_length=10,
    )
    first_name = models.CharField(
        max_length=100,
        editable=False,
    )
    last_name = models.CharField(
        max_length=150,
        editable=False,
    )
    phone_number = models.CharField(
        max_length=13,
    )
    email = models.EmailField(
        max_length=100,
        unique=True,
    )
    gender = models.CharField(
        max_length=100,
        choices=GenderChoices.choices,
    )
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        null=True,
        related_name="members",
    )
    is_coach = models.BooleanField(default=False)

    # @property
    # def _coach(self):
    #     return self.group.coach == self

    def __str__(self) -> str:
        return f"{self.username}"
