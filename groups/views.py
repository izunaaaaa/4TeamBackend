from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Group
from . import serializers
from django.shortcuts import get_object_or_404


class Groups(APIView):
    @swagger_auto_schema(
        operation_summary="그룹 전체 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.GroupSerializer(),
            )
        },
    )
    def get(self, request):
        group = Group.objects.all()
        serializer = serializers.GroupSerializer(group, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="[미완성]그룹 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["name", "coach"],
            properties={
                "name": openapi.Schema(type=openapi.TYPE_STRING, description="그룹명"),
                "coach": openapi.Schema(type=openapi.TYPE_STRING, description="코치정보"),
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


class GroupDetail(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="그룹 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.GroupSerializer(),
            )
        },
    )
    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = serializers.GroupDetailSerializer(group)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="[미완성]그룹 수정 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.GroupSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.GroupSerializer(),
    )
    def put(self, request, pk):
        group = get_object_or_404(Group, pk=pk)
        serializer = serializers.GroupDetailSerializer(
            group,
            data=request.data,
            partial=True,
        )
        if serializer.is_valid():
            group = serializer.save()
            return Response(serializers.GroupDetailSerializer(group).data)
