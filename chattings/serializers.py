from rest_framework.serializers import ModelSerializer
from .models import Chatroom, Message
from users.serializers import TinyUserSerializer
from . import serializers


class ChatroomSerialzier(ModelSerializer):
    user = TinyUserSerializer(read_only=True, many=True)
    # messages = serializers.MessageSerialzier(read_only=True, many=True)

    class Meta:
        model = Chatroom
        fields = (
            "user",
            "created_at",
            # "messages",
        )


class MessageSerialzier(ModelSerializer):
    sender = TinyUserSerializer(read_only=True)
    room = ChatroomSerialzier(read_only=True)

    class Meta:
        model = Message
        fields = (
            "sender",
            "room",
            "text",
        )
