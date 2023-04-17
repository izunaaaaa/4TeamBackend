from rest_framework.serializers import ModelSerializer
from .models import Letter
from users.serializers import TinyUserSerializer
from users.models import User
from rest_framework.exceptions import ValidationError


class LetterSerializer(ModelSerializer):
    sender = TinyUserSerializer(read_only=True)
    receiver = TinyUserSerializer(read_only=True)

    class Meta:
        model = Letter
        fields = (
            "sender",
            "receiver",
            "description",
            "created_at",
            "updated_at",
        )
