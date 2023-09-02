from rest_framework import serializers

import phonenumbers

from .models import *
from utility.fields import *
from .utils.evest import create_customer


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = "__all__"


IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class TemplateSerializer(serializers.ModelSerializer):
    preview_image = serializers.SerializerMethodField()

    def get_preview_image(self, obj):
        if obj.preview_image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.preview_image, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = Template
        fields = "__all__"


class CreativeSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    template = TemplateSerializer()

    class Meta:
        model = Creative
        fields = "__all__"


class AnalyticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Analytics
        fields = "__all__"


class BalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Balance
        fields = "__all__"


class PaymentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentDetail
        fields = "__all__"


class EvestRegistrationSerializer(serializers.Serializer):
    ci = serializers.PrimaryKeyRelatedField(queryset=Creative.objects.all())
    firstName = serializers.CharField()
    lastName = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField()

    def validate_phone(self, value):
        country_code = self.context["country_code"]
        parse_number = phonenumbers.parse(value, country_code)
        number_is_valid = phonenumbers.is_valid_number(parse_number)

        if number_is_valid:
            format_number = phonenumbers.format_number(
                parse_number, phonenumbers.PhoneNumberFormat.E164
            )
        else:
            raise serializers.ValidationError("Phone number not valid!")
        return format_number

    def validate(self, validated_data):
        creative = validated_data.get("ci")
        analytics_obj = self.context["analytics_obj"]
        country_code = self.context["country_code"]

        return super().validate(validated_data)

    def signup(self):
        data = self.validated_data
        country_code = self.context["country_code"]
        user_ip = self.context["user_ip"]
        data["country_code"] = country_code
        data["user_ip"] = user_ip

        create_customer(data)
