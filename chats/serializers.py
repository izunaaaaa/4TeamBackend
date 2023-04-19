from rest_framework.serializers import ModelSerializer
from .models import Chatroom, Message
from users.serializers import TinyUserSerializer


class ChatroomListSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True, many=True)

    class Meta:
        model = Chatroom
        fields = "__all__"


class ChatroomSerialzier(ModelSerializer):
    user = TinyUserSerializer(read_only=True, many=True)

    class Meta:
        model = Chatroom
        fields = "__all__"


class ChatListSerializer(ModelSerializer):
    sender = TinyUserSerializer()

    class Meta:
        model = Message
        fields = "__all__"
