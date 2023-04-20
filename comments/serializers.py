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

    class Meta:
        model = Recomment

        fields = (
            "pk",
            "user",
            "created_at",
            "commentlikeCount",
            "description",
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
        return self.context.get("request").user == data.user


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
            # "feed"
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
        return self.context.get("request").user == data.user
