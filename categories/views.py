from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from .models import Category
from . import serializers
from django.shortcuts import get_object_or_404
from groups.models import Group


class Categories(APIView):
    @swagger_auto_schema(
        operation_summary="카테고리 조회 api",
        manual_parameters=[
            openapi.Parameter(
                "group",
                openapi.IN_QUERY,
                description="그룹 데이터 \n - group의 name로 작성",
                type=openapi.TYPE_STRING,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request):
        group = get_object_or_404(Group, name=request.GET.get("group"))
        category = Category.objects.filter(group=group)
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="카테고리 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            manual_parameters=[
            openapi.Parameter(
                "group",
                openapi.IN_QUERY,
                description="그룹 데이터 \n - group의 name로 작성",
                type=openapi.TYPE_STRING,
            ),
        ],
            required=["name"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="카테고리명"),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def post(self, request):
        serializer = serializers.CategorySerializer(data=request.data)
        
        #만약 request.user이 is_coach가 false인경우
        if request.user.is_coach == False:
            raise PermissionDenied
        
        if serializer.is_valid():
            group = request.GET.get("group")
            group = get_object_or_404(Group, name=group)
            category = serializer.save(group=group)
            serializer = serializers.CategorySerializer(category)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
    
    @swagger_auto_schema(
        operation_summary="카테고리 삭제 api",
        manual_parameters=[
            openapi.Parameter(
                "group",
                openapi.IN_QUERY,
                description="그룹 데이터 \n - group의 name로 작성",
                type=openapi.TYPE_STRING,
            ),
            openapi.Parameter(
                "delete_category_name",
                openapi.IN_QUERY,
                description="삭제할 카테고리 \n - category의 id로 작성",
                type=openapi.TYPE_INTEGER,
            ),
        ],
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.CategorySerializer(many=True),
            )
        },
    )
    def delete(self, request):
        delete_category_id = request.GET.get("delete_category_id")
        Category.objects.get(pk=delete_category_id).delete()
        return Response(status=204)