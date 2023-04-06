from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group
from . import serializers


class Groups(APIView):
    def get(self, request):
        group = Group.objects.all()
        serializer = serializers.GroupSerializer
        return Response(serializer.data)
