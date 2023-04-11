from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "pk",
        "username",
        "is_coach",
        # "_coach",
    )

    fieldsets = (
        (
            "Profile",
            {
                "fields": (
                    "group",
                    "username",
                    "password",
                    "name",
                    "phone_number",
                    "email",
                    "gender",
                    "avatar",
                ),
            },
        ),
        (
            "User Kind",
            {"fields": ("is_coach",)},
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
                "classes": ("collapse",),
            },
        ),
        (
            "Important Dates",
            {
                "fields": ("last_login", "date_joined"),
                "classes": ("collapse",),
            },
        ),
    )
