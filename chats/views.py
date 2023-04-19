from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Chatroom, Message
from . import serializers
from django.shortcuts import get_object_or_404


class ChattingRoomList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅 리스트 조회 api",
        responses={
            200: openapi.Response(
                description="Succfull Response",
                schema=serializers.ChatroomListSerializer(many=True),
            )
        },
    )
    def get(self, request):
        chatlist = Chatroom.objects.filter(user__in=request.user).order_by(
            "-created_at"
        )
        serializer = serializers.ChatroomListSerializer(
            chatlist,
            many=True,
            # context={"request": request},
        )
        return Response(serializer.data)


class ChattingRoom(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅방 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.ChatroomListSerializer(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        chatroom = get_object_or_404(Chatroom, pk=pk)
        serializer = serializers.ChatroomListSerializer(
            chatroom,
            context={"request": request},
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="채팅방 생성 api",
        request_body=openapi.Schema(
            type="None",
            properties={},
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.ChatroomListSerializer(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def post(self, request, pk):
        serializer = serializers.ChatroomSerialzier(data=request.data)
        if serializer.is_valid():
            receiver = request.data.get("receiver")
            if receiver == request.user.pk:
                raise ParseError("자신에게 보낼수 없습니다.")
            if (
                Chatroom.objects.filter(user__in=[request.user])
                .filter(user__in=[receiver])
                .exists()
            ):
                chat_room = (
                    Chatroom.objects.filter(user__in=[request.user]).filter(
                        user__in=[receiver]
                    )
                )[0]
            else:
                chat_room = serializer.save()
                chat_room.user.add(request.user)
                chat_room.user.add(receiver)
            serializer = serializers.ChatroomSerialzier(chat_room)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="채팅방 삭제 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def delete(self, request, pk):
        chatroom = get_object_or_404(Chatroom, pk=pk)
        chatroom.delete()
        return Response("Ok", status=200)


class ChattingList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅 내역 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.ChatListSerializer(many=True),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        room = get_object_or_404(Chatroom, pk=pk)
        if request.user in room.user.all():
            msg = Message.objects.filter(room=room).reverse()
            msg.exclude(sender=request.user).update(is_read=True)
            serializer = serializers.ChatListSerializer(
                msg,
                many=True,
            )
            return Response(serializer.data)
        else:
            raise PermissionDenied
