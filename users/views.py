from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import User
from django.contrib.auth import authenticate, login, logout
from likes.models import Feedlike, Commentlike
from feeds.models import Feed
from likes.serializers import FeedLikeSerializer, CommentLikeSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청 유저의 데이터",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
        },
    )
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="유저 수정 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.PrivateUserSerializer(),
    )
    def put(self, request):
        serilaizer = serializers.PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        if serilaizer.is_valid():
            updated_user = serializer.save()
            if request.data.get("avatar"):
                updated_user.avatar = request.data.get("avatar")
            updated_user.save()
            serializer = serializers.PrivateUserSerializer(updated_user)
            return Response(serilaizer.data)
        else:
            return Response(serializer.errors, status=400)


class UserDetail(APIView):
    @swagger_auto_schema(
        operation_summary="특정 유저 조회 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.TinyUserSerializer(),
            ),
            404: openapi.Response(
                description="User not found",
            ),
        },
    )
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class LogIn(APIView):
    @swagger_auto_schema(
        operation_summary="[미완성]유저 로그인 api",
        responses={200: "OK", 400: "name or password error"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 id ( username )"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 비밀번호"
                ),
            },
        ),
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Invalid username or password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"LogIn": "Success"})
        else:
            return Response({"error": "wrong name or password"}, status=400)


class FeedLikes(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="피드 좋아요 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=FeedLikeSerializer(),
            )
        },
    )
    def get(self, request):
        feedlike = Feedlike.objects.filter(user=request.user)
        serializer = FeedLikeSerializer(
            feedlike,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="피드 좋아요 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["feed"],
            properties={
                "feed": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="피드 id 값"
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
        # feed_pk = request.data.get("feed")
        # feed = self.Feed.objects.get(pk=feed_pk)
        feed = self.get_object(request.data.get("feed"))
        serializer = FeedLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Feedlike.objects.filter(
                user=request.user,
                feed=feed,
            ).exists():
                Feedlike.objects.filter(
                    user=request.user,
                    feed=feed,
                ).delete()
                return Response({"result": "delete success"})
            else:
                feedlike = serializer.save(
                    user=request.user,
                    feed=feed,
                )
                serializer = FeedLikeSerializer(feedlike)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)


class CommentLikes(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="댓글 좋아요 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=CommentLikeSerializer(),
            )
        },
    )
    def get(self, request):
        commentlike = Commentlike.objects.filter(user=request.user)
        serializer = CommentLikeSerializer(
            commentlike,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="댓글 좋아요 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["comment"],
            properties={
                "comment": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="댓글 id 값"
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
        # feed_pk = request.data.get("feed")
        # feed = self.Feed.objects.get(pk=feed_pk)
        feed = self.get_object(request.data.get("feed"))
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Commentlike.objects.filter(
                user=request.user,
                feed=feed,
            ).exists():
                Commentlike.objects.filter(
                    user=request.user,
                    feed=feed,
                ).delete()
                return Response({"result": "delete success"})
            else:
                feedlike = serializer.save(
                    user=request.user,
                    feed=feed,
                )
                serializer = CommentLikeSerializer(feedlike)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
