from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from . import serializers
from .models import Recomment


class Recomments(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        recomment = Recomment.objects.all()
        serializer = serializers.RecommentSerializer(
            recomment,
            many=True,
        )
        return Response(serializer.data)
