from rest_framework.serializers import ModelSerializer
from .models import Feedlike


class FeedLikeSerializer(ModelSerializer):
    class Meta:
        model = Feedlike
        exclude = (
            "created_at",
            "updated_at",
        )
