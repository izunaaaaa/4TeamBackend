from django.contrib import admin
from .models import AccessInfo


# Register your models here.
@admin.register(AccessInfo)
class CommonlikeAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "group",
    )
