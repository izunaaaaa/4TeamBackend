from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from . import serializers


class Comments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="전체 댓글 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CommentSerializer(),
            )
        },
    )
    def get(self, request):
        comment = Comment.objects.all()
        comment = comment.order_by("-created_at")
        serializer = serializers.CommentSerializer(
            comment,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="[미완성]댓글 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "feed", "description"],
            properties={
                "user": openapi.Schema(type=openapi.TYPE_STRING, description="유저정보"),
                "feed": openapi.Schema(type=openapi.TYPE_STRING, description="피드 정보"),
                "description": openapi.Schema(
                    type=openapi.TYPE_STRING, description="내용"
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
        pass
        # serializer = serializers.CommentSerializer(data=request.data)


class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="댓글 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CommentSerializer(),
            )
        },
    )
    def get(self, request, pk):
        comment = self.get_object(pk)
        serializer = serializers.CommentSerializer(comment)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="[미완성]댓글 수정 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.CommentSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.CommentSerializer(),
    )
    def put(serl, request, pk):
        pass
    
    
class TopLikeView(APIView):
    @swagger_auto_schema(
        operation_summary="베스트 댓글 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CommentSerializer(),
            )
        },
    )
    def get(self, request):
        feed = (
        Comment.objects.annotate(like_count=Count("commentlike"))
            .order_by("-like_count").first()
        )
        serializer = serializers.CommentSerializer(feed, many=True)
        return Response(serializer.data)
