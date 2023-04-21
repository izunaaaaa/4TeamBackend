from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Letterlist, Letter
from . import serializers
from users.models import User


class ChattingList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅 목록 조회",
        responses={
            200: openapi.Response(
                description="Succfull Response",
                schema=serializers.ChatroomSerialzier(many=True),
            )
        },
    )
    def get(self, request):
        chatlist = Letterlist.objects.filter(user=request.user).order_by("-created_at")
        serializer = serializers.ChatroomSerialzier(chatlist, many=True)
        return Response(serializer.data)


class ChattingRoom(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅 조회",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.ChatroomSerialzier(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        chatroom = get_object_or_404(Letterlist, pk=pk)
        serializer = serializers.ChatroomSerialzier(
            chatroom,
            context={"request": request},
        )
        return Response(serializer.data)

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
        chatroom = get_object_or_404(Letterlist, pk=pk)
        chatroom.delete()
        return Response("Ok", status=200)


class MessageSend(APIView):
    @swagger_auto_schema(
        operation_summary="채팅방 생성 api",
        request_body=openapi.Schema(
            type="None",
            properties={},
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.ChatroomSerialzier(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def post(self, request):
        serializer = serializers.MessageSerialzier(data=request.data)
        if serializer.is_valid():
            receiver = request.data.get("receiver")
            if not receiver:
                raise ParseError("required receiver")
            if receiver == request.user.pk:
                raise ParseError("can't send to yourself")
            message = serializer.save(sender=request.user, receiver=receiver)
            serializer = serializers.MessageSerialzier(message)
            return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
