from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from .models import AccessInfo
from .serializers import AccessListSerializer
from django.shortcuts import get_object_or_404
from groups.models import Group
from django.db.transaction import atomic
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions


class IsCoachOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_coach or request.user.is_staff


class AllAccessInfo(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="엑세스 가능한 리스트 (임시 테스트용)",
        responses={
            200: openapi.Response(
                schema=AccessListSerializer(many=True),
                description="Successful Response",
            ),
        },
    )
    def get(self, request):
        all_access_info = AccessInfo.objects.all()
        serializer = AccessListSerializer(all_access_info, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="그룹과 엑세스 가능한 유저 생성",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["group", "members"],
            properties={
                "group": openapi.Schema(type=openapi.TYPE_STRING, description="그룹명"),
                "members": openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    description="유저 리스트",
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "name": openapi.Schema(type=openapi.TYPE_STRING),
                            "email": openapi.Schema(type=openapi.TYPE_STRING),
                            "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                            "is_signup": openapi.Schema(
                                type=openapi.TYPE_BOOLEAN,
                                default=False,
                            ),
                        },
                    ),
                ),
            },
        ),
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                        "name": openapi.Schema(type=openapi.TYPE_STRING),
                        "email": openapi.Schema(type=openapi.TYPE_STRING),
                        "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                        "is_signup": openapi.Schema(
                            type=openapi.TYPE_BOOLEAN,
                            default=False,
                        ),
                        "group": openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                "id": openapi.Schema(type=openapi.TYPE_INTEGER),
                                "name": openapi.Schema(type=openapi.TYPE_STRING),
                                "members_count": openapi.Schema(
                                    type=openapi.TYPE_INTEGER
                                ),
                            },
                        ),
                    },
                ),
            ),
            400: openapi.Response(description="Bad Request"),
            500: openapi.Response(description="Internal Server Error"),
        },
    )
    def post(self, request):
        try:
            with atomic():
                group = request.data.get("group")
                members = request.data.get("members")
                if group:
                    group, created = Group.objects.get_or_create(name=group)
                    serializer = AccessListSerializer(data=members, many=True)
                    if serializer.is_valid():
                        serializer = serializer.save(group=group)
                        return Response(
                            AccessListSerializer(serializer, many=True).data
                        )

                    return Response(serializer.errors, status=400)
                else:
                    raise ParseError("Does not exist group")
        except Exception as e:
            return Response({"error": str(e)}, status=500)


class AccessInfoDetail(APIView):
    permission_classes = [IsAuthenticated, IsCoachOrStaff]

    @swagger_auto_schema(
        operation_summary="그룹에 엑세스 가능한 유저 리스트",
        responses={
            200: openapi.Response(
                schema=AccessListSerializer(many=True),
                description="Successful Response",
            ),
        },
    )
    def get(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        access_info = AccessInfo.objects.filter(group=group)
        serializer = AccessListSerializer(access_info, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="엑세스 가능한 유저 추가",
        request_body=openapi.Schema(
            type=openapi.TYPE_ARRAY,
            description="유저 리스트",
            items=openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "name": openapi.Schema(type=openapi.TYPE_STRING),
                    "email": openapi.Schema(type=openapi.TYPE_STRING),
                    "phone_number": openapi.Schema(type=openapi.TYPE_STRING),
                    "is_signup": openapi.Schema(
                        type=openapi.TYPE_BOOLEAN, default=False
                    ),
                },
            ),
        ),
        responses={
            200: openapi.Response(description="Successful Response"),
            400: openapi.Response(description="Bad Request"),
            500: openapi.Response(description="Internal Server Error"),
        },
    )
    def post(self, request, group_pk):
        group = get_object_or_404(Group, pk=group_pk)
        serializer = AccessListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save(group=group)
            return Response("success response")

        else:
            return Response(serializer.errors, status=400)


class AccessInfoDetailUser(APIView):
    permission_classes = [IsAuthenticated, IsCoachOrStaff]

    @swagger_auto_schema(
        operation_summary="그룹에 엑세스 가능한 유저 데이터 조회",
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
        },
    )
    def get(self, request, group_pk, user_pk):
        try:
            user = AccessInfo.objects.get(group__pk=group_pk, pk=user_pk)
        except AccessInfo.DoesNotExist:
            raise NotFound
        serializer = AccessListSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="그룹에 엑세스 가능한 유저 데이터 수정",
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
        },
    )
    def put(self, request, group_pk, user_pk):
        try:
            user = AccessInfo.objects.get(group__pk=group_pk, pk=user_pk)
        except AccessInfo.DoesNotExist:
            raise NotFound

        serializer = AccessListSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)

    @swagger_auto_schema(
        operation_summary="그룹에 엑세스 가능한 유저 데이터 삭제",
        responses={
            200: openapi.Response(
                description="Successful Response",
            ),
        },
    )
    def delete(self, request, group_pk, user_pk):
        try:
            user = AccessInfo.objects.get(group__pk=group_pk, pk=user_pk)
        except AccessInfo.DoesNotExist:
            raise NotFound

        user.delete()
        return Response(status=204)
