from django.contrib import admin
from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    listdisplay = (
        "id",
        "user",
        "group",
        "title",
        "description",
        "visited",
    )

    fieldsets = (
        (
            "User Info",
            {
                "fields": ("user",),
            },
        ),
        (
            "Feed Info",
            {
                "fields": (
                    "group",
                    "title",
                    "description",
                    "visited",
                )
            },
        ),
    )
