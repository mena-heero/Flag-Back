from rest_framework import serializers


from .models import *
from .fields import *
from company.serializers import MinimalCompanySerializer


IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class GlobalSettingsSerializer(serializers.ModelSerializer):
    company_logo = serializers.SerializerMethodField()
    company_logo_large = serializers.SerializerMethodField()

    def get_company_logo(self, obj):
        if obj.company_logo:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.company_logo, IMAGE_RENDITION_RULES
            )
        return None

    def get_company_logo_large(self, obj):
        if obj.company_logo_large:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.company_logo_large, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = GlobalSetting
        fields = "__all__"


class SocialMediaSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialMediaSettings
        fields = "__all__"


class MainMenuItemSerializer(serializers.ModelSerializer):
    company_detail = serializers.SerializerMethodField()
    is_external = serializers.SerializerMethodField()
    get_link = serializers.SerializerMethodField()

    def get_get_link(self, obj):
        return obj.get_link

    def get_company_detail(self, obj):
        if obj.companies:
            from home.page_serializer import CompanyDetailPageSerializer
            return CompanyDetailPageSerializer(obj.companies).data
        return None

    def get_is_external(self, obj):
        return obj.get_is_external

    class Meta:
        model = MainMenuItem
        fields = "__all__"


class MainMenuSerializer(serializers.ModelSerializer):
    submenus = serializers.SerializerMethodField()
    is_external = serializers.SerializerMethodField()

    def get_is_external(self, obj):
        return obj.get_is_external

    def get_submenus(self, obj):
        return MainMenuItemSerializer(
            obj.sub_nav_items.filter(is_active=True), many=True
        ).data

    class Meta:
        model = MainMenu
        fields = "__all__"


class FooterMenuItemSerializer(serializers.ModelSerializer):
    is_external = serializers.SerializerMethodField()

    def get_is_external(self, obj):
        return obj.get_is_external

    class Meta:
        model = FooterMenuItem
        fields = "__all__"


class FooterMenuSerializer(serializers.ModelSerializer):
    submenus = serializers.SerializerMethodField()

    def get_submenus(self, obj):
        return FooterMenuItemSerializer(
            obj.footer_nav_items.filter(is_active=True), many=True
        ).data

    class Meta:
        model = FooterMenu
        fields = "__all__"


class StorySerializer(serializers.ModelSerializer):
    image_detail = serializers.SerializerMethodField()
    image_detail_en = serializers.SerializerMethodField()
    is_external = serializers.SerializerMethodField()

    def get_image_detail(self, obj):
        if obj.image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.image, IMAGE_RENDITION_RULES
            )
        return None

    def get_image_detail_en(self, obj):
        if obj.image_en:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.image_en, IMAGE_RENDITION_RULES
            )
        return None

    def get_is_external(self, obj):
        return obj.get_is_external

    class Meta:
        model = Story
        fields = "__all__"


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = "__all__"


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = "__all__"
