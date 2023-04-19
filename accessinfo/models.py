from django.db import models
from common.models import CommonModel
from groups.models import Group


# Create your models here.
class AccessInfo(CommonModel):
    name = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=13, unique=True)
    email = models.EmailField(max_length=30, unique=True)
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="accessinfo",
    )
    is_signup = models.BooleanField(default=False)
