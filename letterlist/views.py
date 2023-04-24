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


# /me/
class ChattingList(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="채팅방 목록 조회",
        responses={
            200: openapi.Response(
                description="Succfull Response",
                schema=serializers.ChatroomSerialzier(many=True),
            )
        },
    )
    def get(self, request):
        chatlist = Letterlist.objects.filter(user=request.user).order_by("-updated_at")
        serializer = serializers.ChatroomSerialzier(
            chatlist,
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


# /<int:pk>/ GET
class ChattingRoom(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="해당 채팅방의 쪽지 기록 조회",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.MessageSerialzier(),
            ),
            400: openapi.Response(description="Not Found Pk"),
        },
    )
    def get(self, request, pk):
        chat = Letter.objects.filter(room__pk=pk)
        if chat:
            chat = [i for i in chat if request.user not in i.delete_by.all()]
            serializer = serializers.MessageSerialzier(
                chat,
                many=True,
                context={"request": request},
            )

            return Response(serializer.data)
        raise NotFound


# /message/ POST -> 메세지 전송
class MessageSend(APIView):
    @swagger_auto_schema(
        operation_summary="쪽지 전송",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["receiver", "text"],
            properties={
                "receiver": openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    description="보내는 유저의 pk ",
                ),
                "text": openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="전송하는 메세지",
                ),
            },
        ),
        responses={
            201: openapi.Response(
                description="Successful Response",
            ),
            400: openapi.Response(description="Data Error"),
            404: openapi.Response(description="Not Found Pk"),
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
            return Response("Successful Response", status=201)
        else:
            return Response(serializer.errors, status=400)


class MessageDelete(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="쪽지 삭제",
        responses={
            204: openapi.Response(
                description="Successful Response",
            ),
            400: openapi.Response(description="Not Found Pk"),
            403: openapi.Response(description="Sender != request.user"),
        },
    )
    def delete(self, request, pk):
        letter = get_object_or_404(Letter, pk=pk)
        user = [i for i in letter.room.user.all()]
        if request.user in user:
            letter.delete_by.add(request.user)
            letter.save()
        # if letter.sender == request.user:
        #     # letter.delete()
        #     return Response("Ok", status=204)
        else:
            raise PermissionDenied
