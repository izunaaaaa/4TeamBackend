from django.db.models import Q
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Letter
from . import serializers
from django.shortcuts import get_object_or_404
from users.models import User


# from letterlists.models import LetterList
# from django.shortcuts import get_object_or_404


class Letters(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="쪽지 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.LetterSerializer(),
            )
        },
    )
    def get(self, request):
        letter = Letter.objects.filter(
            Q(sender=request.user) | Q(receiver=request.user)
        ).order_by("-updated_at")
        serializer = serializers.LetterSerializer(
            letter,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="쪽지 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["receiver", "description"],
            properties={
                "receiver": openapi.Schema(
                    type=openapi.TYPE_STRING, description="보내는 사람 자동생성"
                ),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="쪽지 내용"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def post(self, request):
        serializer = serializers.LetterSerializer(data=request.data)

        if serializer.is_valid():
            receiver = get_object_or_404(User, username=request.data.get("receiver"))
            if request.user == receiver:
                raise ParseError("cannot send letter to yourself")
            letter = serializer.save(
                sender=request.user,
                receiver=receiver,
            )
            serializer = serializers.LetterSerializer(
                letter,
                many=True,
                context={"request": request},
            )
            return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
