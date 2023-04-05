from django.contrib import admin
from .models import Recomment


@admin.register(Recomment)
class RecommentAdmin(admin.ModelAdmin):
    list_display = ("pk",)
