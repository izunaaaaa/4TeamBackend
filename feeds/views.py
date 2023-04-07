from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, ParseError
from .models import Feed
from . import serializers


class Feeds(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        feed = Feed.objects.all()

        # 최신순
        feed = feed.order_by("-created_at")

        sort = request.GET.get("sort")

        # 인기순
        # if sort == likes:
        #     feed = feed.order_by("-likes")

        # pagenation
        page_size = 10
        page = int(request.query_params.get("page", 1))
        start = (page - 1) * page_size
        end = start + page_size
        paged_feed = feed[start:end]

        # result
        serializer = serializers.FeedSerializer(
            paged_feed,
            many=True,
        )
        return Response(
            {"page_size": page_size, "now_page": page, "data": serializer.data}
        )


class FeedDetail(APIView):

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Feed.objects.get(pk=pk)
        except Feed.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        feed = self.get_object(pk)
        feed.visited += 1
        feed.save()

        serializer = serializers.FeedSerializer(feed)
        return Response(serializer.data)
