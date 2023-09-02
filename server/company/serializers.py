from rest_framework import serializers


from .models import *
from utility.fields import *
from authentication.serializers import MinimalUserSerializer


IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class CompanySerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()
    background_image_detail = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    def get_background_image_detail(self, obj):
        if obj.background_image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.background_image, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = Company
        fields = "__all__"


class MinimalCompanySerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = Company
        fields = ("name", "logo_detail", "rating")


class HomeCompanySerializer(serializers.ModelSerializer):
    background_image_detail = serializers.SerializerMethodField()

    def get_background_image_detail(self, obj):
        if obj.background_image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.background_image, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = Company
        fields = (
            "background_image_detail",
            "account_open_link",
            "is_islamic",
            "rating",
            "slug",
        )


class RatingReviewSerializer(serializers.ModelSerializer):
    user = MinimalUserSerializer(read_only=True)

    class Meta:
        model = RatingReview
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["user"]
        if user:
            validated_data["user"] = user
        return super().create(validated_data)


class StockSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = Stock
        fields = "__all__"


class SavedTopicSerializer(serializers.ModelSerializer):
    article_detail = serializers.SerializerMethodField()

    def get_article_detail(self, obj):
        from .page_serialize import ArticleDetailPageSerializer

        if obj.articles:
            return ArticleDetailPageSerializer(obj.articles).data
        return None

    class Meta:
        model = SavedTopic
        fields = "__all__"

    def create(self, validated_data):
        user = self.context["user"]
        if user:
            validated_data["user"] = user

        obj, created = SavedTopic.objects.get_or_create(
            user=user, articles=validated_data.get("articles"))
        if created:
            obj.type = validated_data.get("type")

        return obj
