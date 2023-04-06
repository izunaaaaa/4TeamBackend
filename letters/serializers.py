from rest_framework.serializers import ModelSerializer
from .models import Letter


class LetterSerializer(ModelSerializer):
    class Meta:
        model = Letter
        fields = "__all__"
