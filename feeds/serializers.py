from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from .models import Feed
from users.serializers import TinyUserSerializer
from comments.serializers import CommentSerializer
from medias.serializers import MediaSerializer
from likes.models import Feedlike
from groups.serializers import GroupSerializer
from categories.serializers import CategorySerializer


class FeedSerializer(ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    # user = TinyUserSerializer(read_only=True)
    # images = MediaSerializer(many=True, read_only=True)
    is_like = SerializerMethodField()
    group = GroupSerializer(read_only=True)
    # category = CategorySerializer(read_only=True)
    highest_like_comments = CommentSerializer(many=True, read_only=True)

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
            "like_count",
            "comments_count",
            "highest_like_comments",          
            "is_like",
            "thumbnail",
        )

    def get_is_like(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Feedlike.objects.filter(
                    user=request.user,
                    feed__pk=data.pk,
                ).exists()
        return False


class FeedDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    comment = CommentSerializer(many=True, read_only=True)
    is_like = SerializerMethodField()
    highest_like_comments = CommentSerializer(many=True, read_only=True)

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
            "updated_at",
            "like_count",
            "comments_count",
            "highest_like_comments",
            "is_like",
            "comment",
            "images",
        )

    def get_is_like(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Feedlike.objects.filter(
                    user=request.user,
                    feed__pk=data.pk,
                ).exists()
        return False
