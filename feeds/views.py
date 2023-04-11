from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.core.paginator import Paginator
from django.db.models import Count
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
        manual_parameters=[
            openapi.Parameter(
                "page",
                openapi.IN_QUERY,
                description="1 페이지당 24개의 데이터 \n - total_pages : 총 페이지수 \n - now_page : 현재 페이지 \n - count : 총 개수 \n - results : 순서",
                type=openapi.TYPE_INTEGER,
            ),
        ],
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
        
        # pagenations
        current_page = request.GET.get("page", 1)
        items_per_page = 10
        paginator = Paginator(feed, items_per_page)
        try:
            page = paginator.page(current_page)
        except:
            page = paginator.page(paginator.num_pages)
        
        if int(current_page) > int(paginator.num_pages):
            raise ParseError("that page is out of range")

        serializer = serializers.FeedSerializer(
            page,
            many=True,
            context={"request": request},
        )

        data = {
            "total_pages": paginator.num_pages,
            "now_page": page.number,
            "count": paginator.count,
            "results": serializer.data,
        }
        
        return Response(data)


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

class TopLikeView(APIView):
    @swagger_auto_schema(
        operation_summary="피드 전체 조회(좋아요순) api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.FeedSerializer(),
            )
        },
    )
    def get(self, request):
        feed = (
            Feed.objects.annotate(like_count=Count("feedlike"))
            .order_by("-like_count")
        )
        serializer = serializers.FeedSerializer(feed, many=True)
        return Response(serializer.data)