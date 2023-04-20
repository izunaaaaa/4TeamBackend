from django.contrib import admin
from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "members_count",
        "stand_by_members_count",
    )
