from django.contrib import admin
from .models import Image


@admin.register(Image)
class Image(admin.ModelAdmin):
    list_display = (
        "pk",
        "url",
    )
