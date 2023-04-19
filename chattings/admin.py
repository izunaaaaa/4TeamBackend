from django.contrib import admin
from .models import Chat, Chattingroom


@admin.register(Chattingroom)
class ChattingroomAdmin(admin.ModelAdmin):
    list_display = ("pk",)


@admin.register(Chat)
class ChatAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "chattingroom",
    )
