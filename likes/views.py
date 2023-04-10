from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import Feedlike, Commentlike
from feeds.models import Feed


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
                schema=serializers.FeedLikeSerializer(),
            )
        },
    )
    def get(self, request):
        feedlike = Feedlike.objects.filter(user=request.user)
        serializer = serializers.FeedLikeSerializer(
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
        serializer = serializers.FeedLikeSerializer(data=request.data)
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
                serializer = serializers.FeedLikeSerializer(feedlike)
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
                schema=serializers.CommentLikeSerializer(),
            )
        },
    )
    def get(self, request):
        commentlike = Commentlike.objects.filter(user=request.user)
        serializer = serializers.CommentLikeSerializer(
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
        serializer = serializers.CommentLikeSerializer(data=request.data)
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
                serializer = serializers.CommentLikeSerializer(feedlike)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
