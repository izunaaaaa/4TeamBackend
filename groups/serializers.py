from rest_framework.serializers import ModelSerializer
from .models import Group
from rest_framework import serializers


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        # exclude = (
        #     "created_at",
        #     "updated_at",
        # )
        fields = (
            "pk",
            "name",
            "members_count",
        )


class GroupDetailSerializer(ModelSerializer):
    members_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Group
        fields = "__all__"
