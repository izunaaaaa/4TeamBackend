from rest_framework.serializers import ModelSerializer
from .models import Comment


class CommentSerializer(ModelSerializer):
    print(1)
    class Meta:
        model = Comment
        exclude = ("updated_at",)
