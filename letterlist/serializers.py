from rest_framework.serializers import ModelSerializer
from .models import Letterlist

class LetterlistSerializer(ModelSerializer):
    class Meta:
        model = Letterlist
        fields = "__all__"