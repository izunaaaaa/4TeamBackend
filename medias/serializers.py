from rest_framework.serializers import ModelSerializer
from .models import Image


class MediaSerializer(ModelSerializer):
    class Meta:
        model = Image
        fields = ("url",)
