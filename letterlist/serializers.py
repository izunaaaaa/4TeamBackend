from rest_framework.serializers import ModelSerializer
from .models import Letter, Letterlist
from users.serializers import TinyUserSerializer
from users.models import User
from django.shortcuts import get_object_or_404


class ChatroomSerialzier(ModelSerializer):
    user = TinyUserSerializer(read_only=True, many=True)
    # messages = serializers.MessageSerialzier(read_only=True, many=True)

    class Meta:
        model = Letterlist
        fields = (
            "user",
            "created_at",
            # "messages",
        )


class MessageSerialzier(ModelSerializer):
    sender = TinyUserSerializer(read_only=True)
    room = ChatroomSerialzier(read_only=True)

    class Meta:
        model = Letter
        fields = (
            "sender",
            "room",
            "text",
        )

    def create(self, validated_data):
        # 유저가 유효한지 확인
        validated_data["receiver"] = get_object_or_404(
            User, pk=validated_data.get("receiver")
        )

        chatroom = (
            Letterlist.objects.filter(user__in=[validated_data.get("sender")])
            .filter(user__in=[validated_data.get("receiver")])
            .first()
        )
        print(chatroom)

        if not chatroom:
            chatroom = Letterlist.objects.create()
            chatroom.user.add(validated_data.get("sender"))
            chatroom.user.add(validated_data.get("receiver"))

        return Letter.objects.create(
            room=chatroom,
            sender=validated_data.get("sender"),
            text=validated_data.get("text"),
        )
