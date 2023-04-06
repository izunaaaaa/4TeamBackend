from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Comment
from . import serializers


class Comments(APIView):
    def get(self, request):
        comment = Comment.objects.all()
        serilaizer = serilaizers.CommentSerializer(comment)
        return Responser(serializer.data)

    def post(self, request):
        serializer = serializers.CommentSerializer(data=request.data)


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
