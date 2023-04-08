from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Group
from . import serializers


class Groups(APIView):
    def get(self, request):
        group = Group.objects.all()
        serializer = serializers.GroupSerializer(group, many=True)
        return Response(serializer.data)


class GroupDetail(APIView):
    def get_object(self, pk):
        try:
            return Group.objects.get(pk=pk)
        except Group.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        group = self.get_object(pk)
        serializer = serializers.GroupSerializer(group)
        return Response(serializer.data)
