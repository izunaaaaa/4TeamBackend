from rest_framework.serializers import ModelSerializer
from .models import Category
from groups.serializers import GroupSerializer
from django.shortcuts import get_object_or_404
from groups.models import Group
from rest_framework.exceptions import ValidationError


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        exclude = (
            "created_at",
            "updated_at",
            "group",
        )

    def create(self, validated_data):
        group = get_object_or_404(Group, pk=validated_data.get("group"))
        validated_data["group"] = group
        category, created = Category.objects.get_or_create(**validated_data)
        if not created:
            # 기존 객체가 이미 존재하는 경우, 예외 처리 등을 수행할 수 있습니다.
            raise ValidationError("Category already exists.")
        return category

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.save()
        return instance
