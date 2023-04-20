from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import Feedlike, Commentlike
from feeds.models import Feed
from django.shortcuts import get_object_or_404
from comments.models import Comment, Recomment


class FeedLikes(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="피드 좋아요 생성 / 삭제",
        responses={
            200: openapi.Response(description="created / deleted"),
            401: openapi.Response(description="The user is not authenticated"),
            404: openapi.Response(description="Not exist Pk"),
        },
    )
    def post(self, request, pk):
        feed = get_object_or_404(Feed, pk=pk)
        like, created = Feedlike.objects.get_or_create(user=request.user, feed=feed)
        like.delete() if not created else None
        return Response({"created" if created else "deleted"})


class CommentLikes(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="댓글 좋아요 생성 / 삭제",
        responses={
            200: openapi.Response(description="created / deleted"),
            401: openapi.Response(description="The user is not authenticated"),
            404: openapi.Response(description="Not exist Pk"),
        },
    )
    def post(self, request, pk):
        comment = get_object_or_404(Comment, pk=pk)
        like, created = Commentlike.objects.get_or_create(
            user=request.user, comment=comment
        )
        like.delete() if not created else None
        return Response({"created" if created else "deleted"})


class ReCommentLikes(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="대댓글 좋아요 생성 / 삭제",
        responses={
            200: openapi.Response(description="created / deleted"),
            401: openapi.Response(description="The user is not authenticated"),
            404: openapi.Response(description="Not exist Pk"),
        },
    )
    def post(self, request, pk):
        recomment = get_object_or_404(Recomment, pk=pk)
        like, created = Commentlike.objects.get_or_create(
            user=request.user, recomment=recomment
        )
        like.delete() if not created else None
        return Response({"created" if created else "deleted"})
