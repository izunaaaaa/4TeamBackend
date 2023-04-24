from rest_framework.serializers import ModelSerializer
from .models import Comment, Recomment
from users.serializers import TinyUserSerializer
from rest_framework.serializers import SerializerMethodField
from likes.models import Commentlike
from . import serializers


class RecommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    is_like = SerializerMethodField()
    is_writer = SerializerMethodField()
    # anonymous_number = SerializerMethodField()

    class Meta:
        model = Recomment

        fields = (
            "pk",
            "user",
            "created_at",
            "commentlikeCount",
            "description",
            # "anonymous_number",
            "is_like",
            "is_writer",
        )

    def get_is_like(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Commentlike.objects.filter(
                    user=request.user,
                    recomment__pk=data.pk,
                ).exists()
        return False

    def get_is_writer(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.user
        return False

    # def get_anonymous_number(self, obj):
    #     comments = Comment.objects.filter(feed=obj.comment.feed)
    #     recomments = Recomment.objects.filter(comment__in=comments)
    #     queryset = list(obj.comment for obj in recomments) + list(comments)
    #     queryset.sort(key=lambda obj: obj.created_at)
    #     for i in queryset:
    #         print(i.user)
    #     return False


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    recomment = serializers.RecommentSerializer(read_only=True, many=True)
    is_like = SerializerMethodField()
    is_writer = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "user",
            "description",
            "created_at",
            "commentlikeCount",
            "recomment",
            "is_like",
            "is_writer",
        )

    def get_is_like(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Commentlike.objects.filter(
                    user=request.user,
                    comment__pk=data.pk,
                ).exists()
        return False

    def get_is_writer(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.user
        return False


class TinyCommentSerializer(ModelSerializer):
    recomment = serializers.RecommentSerializer(read_only=True, many=True)
    is_writer = SerializerMethodField()
    feed = SerializerMethodField()

    class Meta:
        model = Comment
        fields = (
            "id",
            "description",
            "created_at",
            "commentlikeCount",
            "recomment",
            "feed",
            "is_writer",
        )

    def get_feed(self, obj):
        from feeds.serializers import TinyFeedSerializer

        feed = TinyFeedSerializer(obj.feed).data
        return feed

    def get_is_writer(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.user
        return False
