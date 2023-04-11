from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.serializers import TinyUserSerializer


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            # "feed",
            "description",
            "created_at",
            "commentlikeCount",
        )
