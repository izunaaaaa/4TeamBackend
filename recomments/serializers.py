from rest_framework.serializers import ModelSerializer
from .models import Recomment


class RecommentSerializer(ModelSerializer):
    class Meta:
        model = Recomment
        exclude = ("updated_at",)
