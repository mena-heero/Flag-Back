from rest_framework import serializers

from home.models import ArticleDetailPage
from utility.fields import *

IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class ArticleDetailPageSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()
    html_url = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.thumbnail:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.thumbnail, IMAGE_RENDITION_RULES
            )
        return None

    def get_html_url(self, obj):
        return obj.get_url()

    def get_category(self, obj):
        if obj:
            parent = obj.get_parent()
            return {
                "id": parent.specific.id,
                "title": parent.specific.title,
                "slug": parent.specific.slug,
            }
        return None

    class Meta:
        model = ArticleDetailPage
        fields = (
            "title",
            "logo_detail",
            "html_url",
            "first_published_at",
            "category"
        )
