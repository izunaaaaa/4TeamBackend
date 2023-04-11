from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, ParseError
from .models import AccessInfo
from .serializers import AccessInfoSerializer


class AllAccessInfo(APIView):
    def get(self, request):
        all_access_info = AccessInfo.objects.all()
        serializer = AccessInfoSerializer(all_access_info, many=True)
        return Response(serializer.data)
