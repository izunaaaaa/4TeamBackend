from rest_framework.serializers import ModelSerializer
from .models import Comment, Recomment
from users.serializers import TinyUserSerializer
from rest_framework.serializers import SerializerMethodField
from likes.models import Commentlike
from . import serializers


class RecommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)

    class Meta:
        model = Recomment
        fields = (
            "pk",
            "user",
            "created_at",
            "description",
        )


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    recomment = serializers.RecommentSerializer(read_only=True, many=True)
    is_like = SerializerMethodField()

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
