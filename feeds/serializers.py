from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import SerializerMethodField
from .models import Feed
from users.serializers import TinyUserSerializer
from comments.serializers import CommentSerializer
from likes.models import Feedlike
from groups.serializers import GroupSerializer
from categories.serializers import CategorySerializer
from medias.models import Image
from rest_framework.exceptions import ValidationError
import re
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from categories.models import Category
from django.core.cache import cache


class TinyFeedSerializer(ModelSerializer):
    class Meta:
        model = Feed
        fields = (
            "id",
            "title",
            "thumbnail",
            "like_count",
            "comments_count",
        )


class FeedSerializer(ModelSerializer):
    # comment = CommentSerializer(many=True, read_only=True)
    user = TinyUserSerializer(read_only=True)
    # images = MediaSerializer(many=True, read_only=True)
    is_like = SerializerMethodField()
    # group = GroupSerializer(read_only=True)
    is_writer = SerializerMethodField()
    # user = SerializerMethodField()

    class Meta:
        model = Feed
        fields = (
            "id",
            "user",
            # "group",
            # "category",
            "title",
            "visited",
            "created_at",
            "like_count",
            "comments_count",
            "is_like",
            "thumbnail",
            "is_writer",
            # "images",
        )

    def get_is_like(self, data):
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return Feedlike.objects.filter(user=request.user, feed=data).exists()
        return False

    def get_is_writer(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.user
        return False

    def validate_url(self, value):
        # Define a regular expression for valid URLs
        regex = r"^https?://(?:www\.)?\w+\.\w{2,}$"
        # Compile the regular expression into a pattern object
        pattern = re.compile(regex)
        # Attempt to match the URL against the pattern
        match = pattern.match(value)
        if not match:
            raise ValidationError(
                "The URL is not in a valid format.\nPlease ensure that it includes the 'http://' or 'https://' prefix and does not contain any invalid characters."
            )

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        with atomic():
            feed = super().create(validated_data)
            if image:
                self.validate_url(image)
                Image.objects.create(feed=feed, url=image)
            return feed


class FeedDetailSerializer(ModelSerializer):
    user = TinyUserSerializer(read_only=True)
    group = GroupSerializer(read_only=True)
    # comment = SerializerMethodField()
    comment = CommentSerializer(many=True, read_only=True)
    is_like = SerializerMethodField()
    highest_like_comments = CommentSerializer(many=True, read_only=True)
    # images = MediaSerializer(many=True, read_only=True)
    is_writer = SerializerMethodField()

    class Meta:
        model = Feed
        fields = (
            "id",
            "user",
            "group",
            "category",
            "title",
            "description",
            "visited",
            "created_at",
            "updated_at",
            "like_count",
            "thumbnail",
            "comments_count",
            "highest_like_comments",
            "comment",
            # "images",
            "is_like",
            "is_writer",
        )

    # def get_comment(self, obj):
    #     result = CommentSerializer(obj.comment.all(), many=True).data
    #     tmp = [i for i in result]
    #     for i in tmp:
    #         print(type(i))
    #     return CommentSerializer(obj.comment.all(), many=True).data

    def get_is_like(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return Feedlike.objects.filter(
                    user=request.user,
                    feed__pk=data.pk,
                ).exists()
        return False

    def get_is_writer(self, data):
        request = self.context.get("request")
        if request:
            if request.user.is_authenticated:
                return request.user == data.user
        return False

    def validate_url(self, value):
        # Define a regular expression for valid URLs
        regex = r"^https?://(?:www\.)?.+\..{2,}$"
        # Compile the regular expression into a pattern object
        pattern = re.compile(regex)
        # Attempt to match the URL against the pattern
        value = str(value)
        match = pattern.match(value)
        if not match:
            raise ValidationError(
                "The URL is not in a valid format.\nPlease ensure that it includes the 'http://' or 'https://' prefix and does not contain any invalid characters."
            )

    def create(self, validated_data):
        image = validated_data.pop("image", None)
        with atomic():
            feed = super().create(validated_data)
            if image:
                self.validate_url(image)
                Image.objects.create(feed=feed, url=image)
            return feed

    def update(self, instance, validated_data):
        with atomic():
            instance.title = validated_data.get("title", instance.title)
            instance.description = validated_data.get(
                "description", instance.description
            )
            try:
                image = validated_data["image"]
                if image:
                    self.validate_url(image)
                    new_image = Image.objects.get_or_create(feed=instance)[0]
                    new_image.url = image
                    new_image.save()
                else:
                    Image.objects.filter(feed=instance).delete()
            except KeyError:
                pass
            category = validated_data.get("category", instance.category)
            if category:
                if category != instance.category:
                    category = get_object_or_404(Category, pk=category)
                    if category.group != instance.category.group:
                        raise ValidationError("Wrong Category")
                    if category.name == "전체글" or category.name == "인기글":
                        raise ValidationError("전체글과 인기글 카테고리는 선택할수 없습니다.")
                    instance.category = category
            instance.save()
        return instance
