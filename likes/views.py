from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from . import serializers
from .models import Feedlike
from feeds.models import Feed


class FeedLikes(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        feedlike = Feedlike.objects.filter(user=request.user)
        serializer = serializers.FeedLikeSerializer(
            feedlike,
            many=True,
        )
        return Response(serializer.data)

    def post(self, request):
        feed = request.data.get("feed")
        serializer = serializers.FeedLikeSerializer(data=request.data)
        if serializer.is_valid():
            if Feedlike.objects.filter(
                user=request.user,
                feed=feed,
            ).exists():
                Feedlike.objects.filter(
                    user=request.user,
                    feed=feed,
                ).delete()
                return Response({"result": "delete success"})
            else:
                feed = serializer.save(
                    user=request.user,
                    feed=feed,
                )
                serializer = serializers.FeedLikeSerializer(feed)
                return Response({"result": "create success"})
        else:
            return Response(serializer.errors, status=400)
