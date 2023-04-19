from django.contrib import admin
from .models import Chatroom, Message


# Register your models here.
@admin.register(Chatroom)
class Chatting_RoomAdmin(admin.ModelAdmin):
    list_display = ("pk",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender",)
