from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import Feed


class FeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = "__all__"
