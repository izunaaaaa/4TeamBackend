from django.contrib import admin
from .models import Comment, Recomment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "feed",
        "description",
        "commentlikeCount",
    )


@admin.register(Recomment)
class RecommentAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "user",
        "comment",
        "commentlikeCount",
    )
