from rest_framework.serializers import ModelSerializer
from .models import AccessInfo


class AccessListSerializer(ModelSerializer):
    class Meta:
        model = AccessInfo
        exclude = (
            "created_at",
            "updated_at",
        )
