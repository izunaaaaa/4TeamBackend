from rest_framework.serializers import ModelSerializer
from .models import Comment
from users.serializers import TinyUserSerializer
from recomments.serializers import RecommentSerializer
from rest_framework.serializers import SerializerMethodField
from likes.models import Commentlike


class CommentSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    recomment = RecommentSerializer(read_only=True, many=True)
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
