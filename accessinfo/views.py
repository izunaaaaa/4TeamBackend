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


class AllAccessInfo(APIView):
    def get(self, request):
        all_access_info = AccessInfo.objects.all()
        serializer = AccessListSerializer(all_access_info, many=True)
        return Response(serializer.data)


class AccessInfoDetail(APIView):
    def get(self, request, group):
        group = get_object_or_404(Group, name=group)
        access_info = AccessInfo.objects.filter(group=group)
        serializer = AccessListSerializer(access_info, many=True)
        return Response(serializer.data)

    def post(self, request, group):
        group = get_object_or_404(Group, name=group)
        serializer = AccessListSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer = serializer.save(group=group)
            return Response(AccessListSerializer(serializer, many=True).data)

        else:
            return Response(serializer.errors, status=400)
