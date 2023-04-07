from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Comment
from . import serializers


class Comments(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        comment = Comment.objects.all()
        serializer = serializers.CommentSerializer(
            comment,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        pass
        # serializer = serializers.CommentSerializer(data=request.data)


class CommentDetail(APIView):
    def get_object(self, pk):
        try:
            Comment.objects.get(pk=pk)
        except Comment.DoesNotExist:
            raise NotFound

    def get(serl, request, pk):
        pass

    def put(serl, request, pk):
        pass
