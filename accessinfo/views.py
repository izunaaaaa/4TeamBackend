from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError, PermissionDenied
from .models import AccessInfo
from .serializers import AccessListSerializer
from django.shortcuts import get_object_or_404
from groups.models import Group
from django.db import transaction
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated
from rest_framework import authentication, permissions
from django.core.cache import cache


class IsCoachOrStaff(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_coach or request.user.is_staff


class AllAccessInfo(APIView):
    permission_classes = [IsAuthenticated, IsCoachOrStaff]

    def check_duplicate(self, check_list):
        set_check_list = set(check_list)
        if len(set_check_list) != len(check_list):
            raise ParseError("중복된 값이 있습니다.")

    # @swagger_auto_schema(
    #     operation_summary="엑세스 가능한 리스트 (임시 테스트용)",
    #     responses={
    #         200: openapi.Response(
    #             schema=AccessListSerializer(many=True),
    #             description="Successful Response",
    #         ),
    #     },
    # )
    # def get(self, request):
    #     all_access_info = AccessInfo.objects.all()
    #     serializer = AccessListSerializer(all_access_info, many=True)
    #     return Response(serializer.data)

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
        },
    )
    def post(self, request):
        try:
            with transaction.atomic():
                group = request.data.get("group")
                members = request.data.get("members")
                if group:
                    serializer = AccessListSerializer(data=members, many=True)
                    if serializer.is_valid():
                        group, created = Group.objects.get_or_create(name=group)
                        phone_numbers = [i.get("phone_number") for i in members]
                        emails = [i.get("email") for i in members]
                        self.check_duplicate(phone_numbers)
                        self.check_duplicate(emails)
                        serializer = serializer.save(group=group)
                        return Response(
                            AccessListSerializer(serializer, many=True).data
                        )
                    else:
                        return Response(serializer.errors, status=400)
                else:
                    raise ParseError("Does not exist group", 400)
        except Exception as e:
            return Response({"error": str(e)}, status=400)


class AccessInfoDetail(APIView):
    permission_classes = [IsAuthenticated, IsCoachOrStaff]

    def check_duplicate(self, check_list):
        set_check_list = set(check_list)
        if len(set_check_list) != len(check_list):
            raise ParseError("중복된 값이 있습니다.")

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
        if not request.user.is_staff:
            if not request.user.group.pk == group_pk:
                raise PermissionDenied
        group = cache.get(f"group_{group_pk}_access_list")
        if group:
            return Response(group)
        group = get_object_or_404(Group, pk=group_pk)
        access_info = AccessInfo.objects.filter(group=group)
        serializer = AccessListSerializer(access_info, many=True)
        cache.set(f"group_{group_pk}_access_list", serializer.data)
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
        if not request.user.is_staff:
            if not request.user.group.pk == group_pk:
                raise PermissionDenied
        group = get_object_or_404(Group, pk=group_pk)
        if isinstance(request.data, dict):
            serializer = AccessListSerializer(data=request.data)
        elif isinstance(request.data, list):
            serializer = AccessListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            phone_numbers = [i.get("phone_number") for i in request.data]
            emails = [i.get("email") for i in request.data]
            self.check_duplicate(phone_numbers)
            self.check_duplicate(emails)
            serializer.save(group=group)
            cache.delete(f"group_{group_pk}_access_list")
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
        if not request.user.is_staff:
            if not request.user.group.pk == group_pk:
                raise PermissionDenied
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
            cache.delete(f"group_{group_pk}_access_list")
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

        cache.delete(f"group_{group_pk}_access_list")
        return Response(status=204)
