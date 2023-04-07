from rest_framework.serializers import ModelSerializer
from .models import Feedlike, Commentlike


class FeedLikeSerializer(ModelSerializer):
    class Meta:
        model = Feedlike
        exclude = (
            "created_at",
            "updated_at",
            "user",
        )


class CommentLikeSerializer(ModelSerializer):
    class Meta:
        model = Commentlike
        exclude = (
            "created_at",
            "updated_at",
            "user",
        )
