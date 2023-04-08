from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from .models import Letterlist

class Letterlist(APIView):
    def get(self,request):
        letterlist = Letterlist.objects.all()
        serialzier = serialziers.LetterliseSerialzer(letterlist)
        return Response(serialzier.data)