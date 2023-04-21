from django.contrib import admin
from .models import Chattingroom, Message


# Register your models here.
@admin.register(Chattingroom)
class Chatting_RoomAdmin(admin.ModelAdmin):
    list_display = (
        "pk",
        "users_list",
    )


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = (
        "sender",
        "text",
    )
