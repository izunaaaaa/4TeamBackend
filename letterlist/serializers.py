from rest_framework.serializers import ModelSerializer
from .models import Letter, Letterlist
from users.serializers import TinyUserSerializer
from users.models import User
from django.shortcuts import get_object_or_404
from rest_framework.serializers import SerializerMethodField
from rest_framework.exceptions import ParseError


class ChatroomSerialzier(ModelSerializer):
    receiver = SerializerMethodField()
    receiver_pk = SerializerMethodField()

    class Meta:
        model = Letterlist
        fields = (
            # "user",
            "pk",
            "receiver",
            "receiver_pk",
            "created_at",
            "letter_count",
            "last_letter",
        )

    def get_receiver(self, obj):
        request = self.context.get("request")
        for i in obj.user.all():
            if i != request.user:
                return f"{i.username}님과의 쪽지내역"
        raise ParseError("Error")

    def get_receiver_pk(self, obj):
        request = self.context.get("request")
        for i in obj.user.all():
            if i != request.user:
                return i.pk
        raise ParseError("Error")


class MessageSerialzier(ModelSerializer):
    # sender = TinyUserSerializer(read_only=True)
    # room = ChatroomSerialzier(read_only=True)
    is_sender = SerializerMethodField()

    class Meta:
        model = Letter
        fields = (
            # "sender",
            # "room",
            "id",
            "text",
            "is_sender",
        )

    def get_is_sender(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.sender
        return False

    def create(self, validated_data):
        # 유저가 유효한지 확인
        validated_data["receiver"] = get_object_or_404(
            User, pk=validated_data.get("receiver")
        )
        print(1)

        chatroom = (
            Letterlist.objects.filter(user__in=[validated_data.get("sender")])
            .filter(user__in=[validated_data.get("receiver")])
            .first()
        )

        if not chatroom:
            chatroom = Letterlist.objects.create()
            chatroom.user.add(validated_data.get("sender"))
            chatroom.user.add(validated_data.get("receiver"))

        return Letter.objects.create(
            room=chatroom,
            sender=validated_data.get("sender"),
            text=validated_data.get("text"),
        )
