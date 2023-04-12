from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Category
from . import serializers
from django.shortcuts import get_object_or_404
from groups.models import Group


class Categories(APIView):

    # permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="전체 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request):
        category = Category.objects.all()
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)
    
class GroupCategories(APIView):
    
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        operation_summary="그룹 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request, group):
        group = get_object_or_404(Group, name=group)
        category = Category.objects.filter(group=group)
        serializer = serializers.CategorySerializer(
            category,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="그룹 카테고리 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
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
    def post(self, request, group):
        serializer = serializers.CategorySerializer(data=request.data)

        # if request.user.is_coach == False:
            # raise PermissionDenied
        if serializer.is_valid():
            category = serializer.save(group=group)
            serializer = serializers.CategorySerializer(category)
            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

class GroupCategoryDetail(APIView):
    @swagger_auto_schema(
        operation_summary="그룹 카테고리 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.CategorySerializer(),
            )
        },
    )
    def get(self, request, pk, group):
        category = get_object_or_404(Category, pk=pk, group__name=group)
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        operation_summary="그룹 카테고리 삭제 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.CategorySerializer(many=True),
            )
        },
    )
    def delete(self, request, pk,group):
        if request.user.is_coach == False:
            raise PermissionDenied
        group = get_object_or_404(Group, name=group)
        category = Category.objects.filter(group=group,pk=pk)
        category.delete()
        return Response({"result":"delete success"})
