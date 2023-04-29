from django.contrib import admin
from .models import Auth_sms


@admin.register(Auth_sms)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "phone_number",
        "auth_number",
    )
