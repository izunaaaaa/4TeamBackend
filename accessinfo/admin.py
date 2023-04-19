from django.contrib import admin
from .models import AccessInfo


# Register your models here.
@admin.register(AccessInfo)
class AccessInfoAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "group",
        "name",
        "phone_number",
        "email",
        "is_signup",
    )
