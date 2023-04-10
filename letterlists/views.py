from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Letterlist


class Letterlists(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="쪽지 목록 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.LetterlistSerializer(),
            )
        },
    )
    def get(self, request):
        letterlist = Letterlist.objects.filter(user=request.user)
        serialzier = serializers.LetterlistSerializer(letterlist)
        return Response(serialzier.data)
