from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.db.models import Count
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment, Recomment
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
            .order_by("-like_count")
            .first()
        )
        serializer = serializers.CommentSerializer(feed, many=True)
        return Response(serializer.data)


class Recomments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="대댓글 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.RecommentSerializer(),
            )
        },
    )
    def get(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        recomment = comment.all()
        serializer = serializers.RecommentSerializer(
            recomment,
            many=True,
        )
        return Response(serializer.data)
