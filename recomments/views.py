from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import ParseError
from . import serializers
from .models import Recomment


class Recomments(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(
        operation_summary="대댓글 조회 api",
        responses={
            200: openapi.Response(
                description="Successful Response",
                schema=serializers.RecommentSerializer(),
            )
        },
    )
    def get(self, request):
        recomment = Recomment.objects.all()
        serializer = serializers.RecommentSerializer(
            recomment,
            many=True,
        )
        return Response(serializer.data)
