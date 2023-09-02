from rest_framework import serializers

from .models import CompanyDetail, CompanyFinderRating, CompanyChooser
from utility.fields import *
from utility.serializers import CountrySerializer

IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class CompanyDetailPageSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = CompanyDetail
        fields = (
            "title",
            "title_en",
            "logo_detail",
            "rating"
        )


class CompanyDetailForFindBrokerSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()
    html_url = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    def get_html_url(self, obj):
        return obj.get_url()

    class Meta:
        model = CompanyDetail
        fields = (
            "id",
            "title",
            "title_en",
            "logo",
            "rating",
            "logo_detail",
            "html_url"
        )


class CompanyDetailForComparisonSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()
    html_url = serializers.SerializerMethodField()
    origin_branch = serializers.SerializerMethodField()

    def get_logo_detail(self, obj):
        if obj.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.logo, IMAGE_RENDITION_RULES
            )
        return None

    def get_html_url(self, obj):
        return obj.get_url()

    def get_origin_branch(self, obj):
        if obj.origin_branch:
            return CountrySerializer(obj.origin_branch).data
        return None

    class Meta:
        model = CompanyDetail
        fields = (
            "id",
            "title",
            "title_en",
            "logo_detail",
            "html_url",
            "overal_evaluation",
            "is_islamic",
            "fees_rating",
            "deposit_withdraw_rating",
            "trading_platforms",
            "markets_products",
            "security_rating",
            "customer_service_rating",
            "research_development_rating",
            "demo_account",
            "leverage",
            "recommendation_text",
            "recommendation_text_en",
            "origin_branch"
        )


class CompanyChooserSerializer(serializers.ModelSerializer):
    logo_detail = serializers.SerializerMethodField()
    html_url = serializers.SerializerMethodField()
    rating = serializers.SerializerMethodField()
    title = serializers.SerializerMethodField()
    title_en = serializers.SerializerMethodField()


    def get_logo_detail(self, obj):
        if obj.company.logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.company.logo, IMAGE_RENDITION_RULES
            )
        return None

    def get_html_url(self, obj):
        if obj.company:
            return obj.company.get_url()
        return None

    def get_rating(self, obj):
        if obj.company:
            return obj.company.rating
        return None

    def get_title(self, obj):
        if obj.company:
            return obj.company.title
        return None

    def get_title_en(self, obj):
        if obj.company:
            return obj.company.title_en
        return None

    class Meta:
        model = CompanyChooser
        fields = (
            "logo_detail",
            "html_url",
            "rating",
            "title",
            "title_en"
        )


class CmpanyFinderRatingSerializer(serializers.ModelSerializer):
    companies = serializers.SerializerMethodField()

    def get_companies(self, obj):
        qs = obj.companies.all()
        return CompanyChooserSerializer(qs, many=True).data

    class Meta:
        model = CompanyFinderRating
        fields = "__all__"
