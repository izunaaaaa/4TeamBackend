from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Letter
from . import serializers


class Letters(APIView):
    def get(self, request):
        letter = Letter.objects.all()
        serializer = serializers.LetterSerializer(letter)
        return Response(serializer.data)
