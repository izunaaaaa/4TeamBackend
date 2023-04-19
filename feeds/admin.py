from django.contrib import admin
from .models import Feed
from categories.models import Category
from django import forms


@admin.register(Feed)
class FeedAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "group",
        "description",
        "comments_count",
    )

    list_display_links = ("id",)

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
                    "category",
                    "description",
                )
            },
        ),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        # Limit category choices to those associated with the group of the feed
        if obj is not None:
            group_categories = Category.objects.filter(group=obj.group)
            form.base_fields["category"].queryset = group_categories
        # If creating a new feed, limit category choices based on the user's group
        else:
            user_categories = Category.objects.all()
            form.base_fields["category"].queryset = user_categories

        return form
