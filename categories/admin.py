from django.contrib import admin
from .models import Category
from django.utils import timezone
import datetime


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "name",
        "group",
        "feed_count",
    )
