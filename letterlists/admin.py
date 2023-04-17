from django.contrib import admin
from .models import Letterlist


@admin.register(Letterlist)
class LetterAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        # "__str__",
        # "sender",
        # "receiver",
    )
