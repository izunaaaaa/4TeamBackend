from django.contrib import admin
from .models import Feed


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "group",
        "title",
        "description",
    )

    fieldsets = (
        (
            "User Info",
            {
                "fields": (
                    "user",
                    "group",
                ),
            },
        ),
        (
            "Feed Info",
            {
                "fields": (
                    "category",
                    "title",
                    "description",
                )
            },
        ),
    )
