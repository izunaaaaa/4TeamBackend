from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Feed
from . import serializers

# from django.shortcuts import get_object_or_404


class Feeds(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="피드 전체 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.FeedSerializer(),
            )
        },
    )
    def get(self, request):
        feed = Feed.objects.all()

        # 최신순
        feed = feed.order_by("-created_at")

        sort = request.GET.get("sort")

        # 인기순
        # if sort == likes:
        #     feed = feed.order_by("-likes")

        # pagenation
        page_size = 10
        page = int(request.query_params.get("page", 1))
        start = (page - 1) * page_size
        end = start + page_size
        paged_feed = feed[start:end]

        # result
        serializer = serializers.FeedSerializer(
            paged_feed,
            many=True,
        )
        return Response(
            {"page_size": page_size, "now_page": page, "data": serializer.data}
        )

    @swagger_auto_schema(
        operation_summary="[미완성]피드 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["user", "group", "title"],
            properties={
                "user": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저정보 자동생성"
                ),
                "group": openapi.Schema(
                    type=openapi.TYPE_STRING, description="그룹정보 자동생성"
                ),
                "title": openapi.Schema(type=openapi.TYPE_STRING, description="타이틀"),
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


class FeedDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="피드 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.FeedSerializer(),
            )
        },
    )
    def get(self, request, pk):
        feed = self.get_object(pk)
        # feed = get_object_or_404(Feed, pk=pk)
        feed.visited += 1
        feed.save()

        serializer = serializers.FeedSerializer(feed)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="[미완성]피드 수정 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.FeedSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.FeedSerializer(),
    )
    def put(self, request, pk):
        pass
