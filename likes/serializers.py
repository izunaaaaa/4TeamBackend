from rest_framework.serializers import ModelSerializer
from .models import Feedlike, Commentlike
from feeds.serializers import TinyFeedSerializer


class FeedLikeSerializer(ModelSerializer):
    feed = TinyFeedSerializer(read_only=True)

    class Meta:
        model = Feedlike
        fields = ("feed",)


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = Commentlike
        exclude = (
            "created_at",
            "updated_at",
            "user",
        )
