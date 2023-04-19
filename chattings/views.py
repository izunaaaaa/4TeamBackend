from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied, ParseError
from rest_framework.permissions import IsAuthenticated
from .models import Chat, Chattingroom
from . import serializers
from users.models import User


class ChattingRoomList(APIView):
    def get(self, request):
        # chattingroom = Chattingroom.objects.filter(user=request.user)
        chattingroom = Chattingroom.objects.all()
        serializer = serializers.ChattingRoomSerialzier(chattingroom)
        return Response(serializer.data)


class ChattingRoom(APIView):
    def get(self, request, pk):
        chattingroom = get_object_or_404(Chattingroom, pk=pk)
        serializer = serializers.ChattingRoomSerialzier(chattingroom)
        return Response(serializer.data)
