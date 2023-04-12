from rest_framework.serializers import ModelSerializer
from .models import Category
from groups.serializers import GroupSerializer
from django.shortcuts import get_object_or_404
from groups.models import Group
class CategorySerializer(ModelSerializer):
    group = GroupSerializer(read_only=True)
    
    class Meta:
        model = Category
        exclude = (
            "created_at",
            "updated_at",
        )
    
    def create(self,validated_data):
        validated_data["group"] = get_object_or_404(Group, name=validated_data["group"])
        return Category.objects.get_or_create(**validated_data)
