from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Letterlist


class Letterlists(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        letterlist = Letterlist.objects.filter(user=request.user)
        serialzier = serializers.LetterliseSerialzer(letterlist)
        return Response(serialzier.data)
