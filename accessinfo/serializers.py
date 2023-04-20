from rest_framework.serializers import ModelSerializer
from .models import AccessInfo
from groups.serializers import GroupSerializer
import re
from rest_framework import serializers


class AccessListSerializer(ModelSerializer):
    group = GroupSerializer(read_only=True)
    is_signup = serializers.BooleanField(read_only=True)

    class Meta:
        model = AccessInfo
        exclude = (
            "created_at",
            "updated_at",
        )

    def validate_phone_number(self, data):
        phone_regex = re.compile(r"^010\d{4}\d{4}$")
        data = data.replace("-", "")
        if not phone_regex.match(data):
            raise serializers.ValidationError("유효한 형식을 입력하세요.")

        if AccessInfo.objects.filter(phone_number=data).exists():
            raise serializers.ValidationError("이미 존재하는 전화번호입니다.")
        return data

    def validate_email(self, data):
        if AccessInfo.objects.filter(email=data).exists():
            raise serializers.ValidationError("이미 존재하는 이메일입니다.")
        return data
