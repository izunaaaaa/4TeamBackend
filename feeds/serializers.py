from rest_framework.serializers import ModelSerializer
from .models import Feed
from users.serializers import TinyUserSerializer
from comments.serializers import CommentSerializer
from medias.serializers import MediaSerializer

class FeedSerializer(ModelSerializer):
    comment= CommentSerializer(many=True,read_only=True)
    user = TinyUserSerializer(read_only=True)
    media = MediaSerializer(many=True, read_only=True)
     
    class Meta:
        model = Feed
        fields = (
            "id",
            "user",
            "group",
            "category",
            "title",
            "description",
            "visited",
            "created_at",
            "comment",
            "media",
        )
