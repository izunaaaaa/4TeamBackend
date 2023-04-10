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
        operation_summary="[미완성]카테고리 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["group", "name"],
            properties={
                "group": openapi.Schema(
                    type=openapi.TYPE_STRING, description="params값으로 자동 입력"
                ),
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
        print(request.GET.get("group"))
        if serializer.is_valid():
            feed = serializer.save()

            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)


# class CategoryDetail(APIView):
#     def get_object(self, pk):
#         try:
#             return Category.objects.get(pk=pk)
#         except Category.DoesNotExist:
#             raise NotFound

#     def get(self, request, pk):
#         category = self.get_object(pk)
#         serializer = serializers.CategorySerializer(
#             category,
#             many=True,
#         )
#         return Response(serializer.data)
