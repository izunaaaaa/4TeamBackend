from rest_framework.serializers import ModelSerializer
from .models import Chat, Chattingroom
from users.serializers import TinyUserSerializer
from . import serializers


class ChatSerialzier(ModelSerializer):
    class Meta:
        model = Chat
        fields = (
            "pk",
            "message",
        )


class ChattingRoomSerialzier(ModelSerializer):
    user = TinyUserSerializer(read_only=True, many=True)
    chat = serializers.ChatSerialzier(read_only=True, many=True)

    class Meta:
        model = Chattingroom
        fields = "__all__"
        # fields = (
        #     "pk",
        #     "user",
        #     "chat",
        # )
