# from drf_yasg import openapi

# from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from . import serializers
from .models import User


class Me(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = serializers.PrivateUserSerializer(user)
        return Response(serializer.data)

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


class UserDetail(APIView):
    def get(self, request, username):
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFound
        serializer = serializers.TinyUserSerializer(user)
        return Response(serializer.data)


class LogIn(APIView):
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
