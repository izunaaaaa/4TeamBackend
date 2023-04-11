from rest_framework.serializers import ModelSerializer
from .models import Feed
from users.serializers import TinyUserSerializer
from comments.serializers import CommentSerializer


class FeedSerializer(ModelSerializer):
    feed_comment = CommentSerializer(many=True,read_only=True)
    user = TinyUserSerializer(read_only=True)
     
    class Meta:
        model = Feed
        # fields = "__all__"
        fields = (
            "id",
            "user",
            "group",
            "category",
            "title",
            "description",
            "visited",
            "created_at",
            "feed_comment",
        )
