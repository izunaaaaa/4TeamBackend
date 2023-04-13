from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.serializers import TinyUserSerializer
from recomments.serializers import RecommentSerializer


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    recomment = RecommentSerializer(read_only=True, many=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            # "feed"
            "description",
            "created_at",
            "commentlikeCount",
            "recomment",
        )
