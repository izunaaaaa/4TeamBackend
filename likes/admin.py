from django.contrib import admin
from .models import Feedlike, Commentlike


@admin.register(Feedlike)
class FeedlikeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "feed",
    )


@admin.register(Commentlike)
class CommonlikeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "comment",
    )
