from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import User
from django.contrib.auth import authenticate, login, logout
from likes.models import Feedlike, Commentlike
from feeds.models import Feed
from likes.serializers import FeedLikeSerializer, CommentLikeSerializer


class Me(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="요청 유저의 데이터",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
        },
    )
    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="유저 수정 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.PrivateUserSerializer(),
            ),
            400: "Bad Request",
        },
        request_body=serializers.PrivateUserSerializer(),
    )
    def put(self, request):
        serilaizer = serializers.PrivateUserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )

        if serilaizer.is_valid():
            updated_user = serializer.save()
            if request.data.get("avatar"):
                updated_user.avatar = request.data.get("avatar")
            updated_user.save()
            serializer = serializers.PrivateUserSerializer(updated_user)
            return Response(serilaizer.data)
        else:
            return Response(serializer.errors, status=400)

    # class UserDetail(APIView):
    @swagger_auto_schema(
        operation_summary="특정 유저 조회 api",
        responses={
            200: openapi.Response(
                description="Successful response",
                schema=serializers.TinyUserSerializer(),
            ),
            404: openapi.Response(
                description="User not found",
            ),
        },
    )
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class LogIn(APIView):
    @swagger_auto_schema(
        operation_summary="[미완성]유저 로그인 api",
        responses={200: "OK", 400: "name or password error"},
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["username", "password"],
            properties={
                "username": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 id ( username )"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 비밀번호"
                ),
            },
        ),
    )
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise ParseError("Invalid username or password")
        user = authenticate(
            request,
            username=username,
            password=password,
        )
        if user:
            login(request, user)
            return Response({"LogIn": "Success"})
        else:
            return Response({"error": "wrong name or password"}, status=400)


class FeedLikes(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="피드 좋아요 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=FeedLikeSerializer(),
            )
        },
    )
    def get(self, request):
        feedlike = Feedlike.objects.filter(user=request.user)
        serializer = FeedLikeSerializer(
            feedlike,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="피드 좋아요 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["feed"],
            properties={
                "feed": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="피드 id 값"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def post(self, request):
        # feed_pk = request.data.get("feed")
        # feed = self.Feed.objects.get(pk=feed_pk)
        feed = self.get_object(request.data.get("feed"))
        serializer = FeedLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Feedlike.objects.filter(
                user=request.user,
                feed=feed,
            ).exists():
                Feedlike.objects.filter(
                    user=request.user,
                    feed=feed,
                ).delete()
                return Response({"result": "delete success"})
            else:
                feedlike = serializer.save(
                    user=request.user,
                    feed=feed,
                )
                serializer = FeedLikeSerializer(feedlike)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)


class CommentLikes(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    @swagger_auto_schema(
        operation_summary="댓글 좋아요 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=CommentLikeSerializer(),
            )
        },
    )
    def get(self, request):
        commentlike = Commentlike.objects.filter(user=request.user)
        serializer = CommentLikeSerializer(
            commentlike,
            many=True,
        )
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_summary="댓글 좋아요 생성 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["comment"],
            properties={
                "comment": openapi.Schema(
                    type=openapi.TYPE_INTEGER, description="댓글 id 값"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def post(self, request):
        # feed_pk = request.data.get("feed")
        # feed = self.Feed.objects.get(pk=feed_pk)
        feed = self.get_object(request.data.get("feed"))
        serializer = CommentLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Commentlike.objects.filter(
                user=request.user,
                feed=feed,
            ).exists():
                Commentlike.objects.filter(
                    user=request.user,
                    feed=feed,
                ).delete()
                return Response({"result": "delete success"})
            else:
                feedlike = serializer.save(
                    user=request.user,
                    feed=feed,
                )
                serializer = CommentLikeSerializer(feedlike)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)


class CheckID(APIView):
    @swagger_auto_schema(
        operation_summary="중복 아이디 체크 api",
        responses={
            200: openapi.Response(
                description="Successful response",
            ),
            409: "Conflct Response",
        },
        manual_parameters=[
            openapi.Parameter(
                name="id",
                in_=openapi.IN_QUERY,
                description="검사할 아이디",
                type=openapi.TYPE_STRING,
                required=True,
            )
        ],
    )
    def get(self, request):
        id = request.GET.get("id")
        if User.objects.filter(username=id).exists():
            return Response(status=409)
        return Response(status=200)


class SignUp(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    @swagger_auto_schema(
        operation_summary="회원가입 api",
        responses={
            201: "Created",
            400: "bad request",
        },
        request_body=serializers.PrivateUserSerializer(),
    )
    def post(self, request):
        password = str(request.data.get("password"))
        if not password:
            raise ParseError("password 가 입력되지 않았습니다.")

        serializer = serializers.PrivateUserSerializer(data=request.data)
        if serializer.is_valid():
            self.validate_password(password)
            user = serializer.save()
            if request.data.get("avatar"):
                user.avatar = request.data.get("avatar")
            user.set_password(password)
            # user.password = password 시에는 raw password로 저장
            user.save()
            # set_password 후 다시 저장
            serializer = serializers.PrivateUserSerializer(user)
            login(request, user)

            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "data": serializer.data,
                },
                status=201,
            )
        else:
            return Response(serializer.errors, status=400)


class ChangePassword(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="비밀번호 수정 api",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=["old_password", "new_password"],
            properties={
                "old_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="현재 비밀번호 입력"
                ),
                "new_password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="새로운 비밀번호 입력"
                ),
            },
        ),
        responses={
            200: openapi.Response(description="OK"),
            400: openapi.Response(description="Invalid request data"),
            401: openapi.Response(description="The user is not authenticated"),
        },
    )
    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        if not old_password or not new_password:
            raise ParseError("Invalid password")
        if user.check_password(old_password):
            self.validate_password(new_password)
            user.set_password(new_password)
            user.save()
            return Response(status=200)
        else:
            return Response(status=400)


class FindId(APIView):
    def post(self, request):
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        if not name or not email or not phone_number:
            raise ParseError("Invalid field")
        try:
            user = User.objects.get(
                name=name,
                email=email,
                phone_number=phone_number,
            )
        except User.DoesNotExist:
            return Response(status=404)

        return Response({"id": user.username}, status=200)


class FindPassword(APIView):
    def post(self, request):
        username = request.data.get("id")
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        if not username or not name or not email or not phone_number:
            raise ParseError("Invalid field")
        try:
            user = User.objects.get(
                username=username,
                name=name,
                email=email,
                phone_number=phone_number,
            )
        except User.DoesNotExist:
            return Response(status=404)
        return Response(status=200)


class NewPassword(APIView):
    def validate_password(self, password):
        REGEX_PASSWORD = "^(?=.*[\d])(?=.*[a-z])(?=.*[!@#$%^&*()])[\w\d!@#$%^&*()]{8,}$"
        if not re.fullmatch(REGEX_PASSWORD, password):
            raise ParseError(
                "비밀번호를 확인하세요. 최소 1개 이상의 소문자, 숫자, 특수문자로 구성되어야 하며 길이는 8자리 이상이어야 합니다."
            )

    def put(self, request):
        username = request.data.get("id")
        name = request.data.get("name")
        email = request.data.get("email")
        phone_number = request.data.get("phone_number")
        password = request.data.get("password")
        if not username or not name or not email or not phone_number or not password:
            raise ParseError("Invalid field")
        try:
            user = User.objects.get(
                username=username,
                name=name,
                email=email,
                phone_number=phone_number,
            )
        except User.DoesNotExist:
            return Response(status=404)

        self.validate_password(password)
        user.set_password(password)
        user.save()
        return Response(status=200)
