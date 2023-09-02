from django.contrib.auth.password_validation import (
    validate_password as dj_validate_password,
)
from django.contrib.auth.hashers import check_password
from django.db import transaction
from django.contrib.auth import authenticate
from django.utils.timezone import now

from rest_framework import serializers
from rest_framework.authtoken.models import Token

import phonenumbers


from .models import *
from .choices import *
from utility.fields import *
from utility.models import Country

IMAGE_RENDITION_RULES = {"original": "original|jpegquality-60|format-webp"}


class UserSerializer(serializers.ModelSerializer):
    profile_image_detail = serializers.SerializerMethodField()

    def get_profile_image_detail(self, obj):
        if obj.profile_image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.profile_image, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = User
        exclude = ("password", "user_permissions", "groups")
        read_only_fields = ("is_email_verified", "is_staff", "is_superuser")

    def update(self, instance, validated_data):
        email_changed = False

        if validated_data.get("email"):
            if instance.email != validated_data["email"]:
                email_changed = True
        user = super().update(instance, validated_data)

        if email_changed == True:
            user.is_email_verified = False
            user.save()
            user.send_verification_code(reason=None, email=instance.email)
        return user


class MinimalUserSerializer(serializers.ModelSerializer):
    profile_image_detail = serializers.SerializerMethodField()

    def get_profile_image_detail(self, obj):
        if obj.profile_image:
            return ImageSerializer.to_representation(
                ImageSerializer, obj.profile_image, IMAGE_RENDITION_RULES
            )
        return None

    class Meta:
        model = User
        fields = ("full_name", "email", "profile_image_detail")


class SignUpSerializer(serializers.Serializer):
    email = serializers.EmailField()
    full_name = serializers.CharField(required=False)
    country = serializers.IntegerField(required=True)
    phone = serializers.CharField(required=True)
    password = serializers.CharField(
        style={"input_type": "password"},
        required=False,
        allow_null=True,
        allow_blank=True,
    )

    def validate_country(self, value):
        country_exists = Country.objects.filter(id=value).exists()
        if country_exists:
            return value
        raise serializers.ValidationError("Invalid country!")

    def validate_password(self, value):
        dj_validate_password(value)
        return value

    def validate(self, validated_data):
        email = validated_data.get("email")
        country = validated_data.get("country")
        phone = validated_data.get("phone")

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email exists!"]})

        country_obj = Country.objects.get(id=country)
        parse_number = phonenumbers.parse(phone, country_obj.alpha_2)
        number_is_valid = phonenumbers.is_valid_number(parse_number)

        if number_is_valid == False:
            raise serializers.ValidationError(
                {"phone": ["Phone number not valid for your country!"]}
            )

        return validated_data

    def create(self, validated_data):
        password = validated_data.pop("password", None)
        country = validated_data.pop("country", None)

        country_obj = Country.objects.get(id=country)

        user = User(**validated_data)
        user.set_password(password)
        user.is_email_verified = True
        user.country = country_obj
        user.save()
        return user


class SendVerificationCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    reason = serializers.CharField(required=False)
    user_checking = serializers.BooleanField(required=False)

    def validate(self, validated_data):
        email = validated_data.get("email")
        user_checking = validated_data.get("user_checking", True)

        if user_checking == True:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": ["Email not found!"]})
        return validated_data

    def send_code(self):
        email = self.validated_data.get("email")
        User.send_verification_code(User, email=email)
        return None


class VerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True)

    def validate(self, validated_data):
        email = validated_data.get("email")
        code = validated_data.get("code")
        user_checking = self.context.get("user_checking", True)
        signup_user = self.context.get("signup_user", None)

        if signup_user:
            if email != signup_user:
                raise serializers.ValidationError({"email": ["Invalid data!"]})

        if user_checking == True:
            if not User.objects.filter(email=email).exists():
                raise serializers.ValidationError({"email": ["Email not found!"]})

        try:
            verification_obj = Verification.objects.get(email=email)
        except:
            verification_obj = None

        if verification_obj is None:
            raise serializers.ValidationError({"email": ["Not found!"]})
        else:
            if verification_obj.code != code:
                raise serializers.ValidationError({"code": ["Invalid code!"]})
        return validated_data

    def verify_code(self):
        email = self.validated_data.get("email")
        code = self.validated_data.get("code")
        user_checking = self.context.get("user_checking", True)

        verification_obj = Verification.objects.get(email=email, code=code)
        verification_obj.code = None
        verification_obj.save()

        if user_checking == True:
            user = User.objects.get(email=email)
            user.is_email_verified = True
            user.save()
            # verify_confirm_email_queue.delay(user.email)
        return True

    def verify_code_signup(self):
        email = self.validated_data.get("email")
        code = self.validated_data.get("code")

        verification_obj = Verification.objects.get(email=email, code=code)
        verification_obj.code = None
        verification_obj.save()
        # verify_confirm_email_queue.delay(user.email)
        return True

    def send_verify_confirm_email(self):
        email = self.validated_data.get("email")
        verify_confirm_email_queue.delay(email)
        return True


class SigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, value):
        dj_validate_password(value)
        return value

    def validate(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")

        user = authenticate(self, username=username, password=password)
        if not user:
            raise serializers.ValidationError(
                {"email": ["Incorrect Email / Password!"]}
            )
        else:
            if not user.is_active:
                raise serializers.ValidationError(
                    {"username": ["Account is blocked! Please contact support!"]}
                )
        return validated_data

    def signin(self):
        username = self.validated_data.get("username")
        password = self.validated_data.get("password")

        user = authenticate(self, username=username, password=password)

        if user.is_email_verified:
            token, token_created = Token.objects.get_or_create(user=user)
            token = token.key
        else:
            token = None

        user.last_login = now()
        user.save()
        return user, token


class AffiliateSigninSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, value):
        dj_validate_password(value)
        return value

    def validate(self, validated_data):
        username = validated_data.get("username")
        password = validated_data.get("password")

        user = authenticate(self, username=username, password=password)

        if user:
            if user.user_type != UserTypeChoice.AFFILIATE:
                raise serializers.ValidationError(
                    {"username": ["You are not allowed to signin!"]}
                )

        if not user:
            raise serializers.ValidationError(
                {"email": ["Incorrect Email / Password!"]}
            )
        else:
            if not user.is_active:
                raise serializers.ValidationError(
                    {"username": ["Account is blocked! Please contact support!"]}
                )
        return validated_data

    def signin(self):
        username = self.validated_data.get("username")
        password = self.validated_data.get("password")

        user = authenticate(self, username=username, password=password)

        if user.is_email_verified and user.user_type == UserTypeChoice.AFFILIATE:
            token, token_created = Token.objects.get_or_create(user=user)
            token = token.key
        else:
            token = None

        user.last_login = now()
        user.save()
        return user, token


class ForgetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.IntegerField(required=True)
    password = serializers.CharField(style={"input_type": "password"})

    def validate_password(self, value):
        dj_validate_password(value)
        return value

    def validate(self, validated_data):
        email = validated_data.get("email")
        code = validated_data.get("code")
        password = validated_data.get("password")

        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email not found!"]})

        try:
            verification_obj = Verification.objects.get(email=email)
        except:
            verification_obj = None

        if verification_obj is None:
            raise serializers.ValidationError({"email": ["Not found!"]})
        else:
            if verification_obj.code != code:
                raise serializers.ValidationError({"code": ["Invalid code!"]})

        return validated_data

    def forget_password(self):
        email = self.validated_data.get("email")
        password = self.validated_data.get("password")

        user = User.objects.get(email=email)
        user.set_password(password)
        user.save()

        verification_obj = Verification.objects.get(email=email)
        verification_obj.code = None
        verification_obj.save()
        return None


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(style={"input_type": "password"})
    new_password = serializers.CharField(style={"input_type": "password"})
    new_password2 = serializers.CharField(style={"input_type": "password"})

    def validate_old_password(self, value):
        user = self.context["user"]
        if not user.check_password(value):
            raise serializers.ValidationError("Old password entered incorrectly!")
        dj_validate_password(value)
        return value

    def validate_new_password(self, value):
        dj_validate_password(value)
        return value

    def validate_new_password2(self, value):
        dj_validate_password(value)
        return value

    def validate(self, validated_data):
        new_password = validated_data.get("new_password")
        new_password2 = validated_data.get("new_password2")

        if new_password != new_password2:
            raise serializers.ValidationError(
                {"new_password": ["The 2 password field not matched!"]}
            )
        return validated_data

    def change_password(self):
        password = self.validated_data.get("new_password")
        user = self.context["user"]
        user.set_password(password)
        user.save()
        return user


class SocialAuthDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialAuthData
        fields = "__all__"


class SocialAuthCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    country = serializers.IntegerField(required=True)
    phone = serializers.CharField(required=True)
    auth_type = serializers.IntegerField(required=True)
    social_id = serializers.CharField(required=False)

    def validate_country(self, value):
        country_exists = Country.objects.filter(id=value).exists()
        if country_exists:
            return value
        raise serializers.ValidationError("Invalid country!")

    def validate_auth_type(self, value):
        available_auth_type = [AuthTypeChoice.GOOGLE, AuthTypeChoice.FACEBOOK]
        if value in available_auth_type:
            return value
        raise serializers.ValidationError("Invalid data! Try again later!")

    def validate_social_id(self, value):
        if value:
            social_data_exists = SocialAuthData.objects.filter(social_id=value).exists()
            if social_data_exists:
                return value
            raise serializers.ValidationError("Invalid data! Try again later!")
        return value

    def validate(self, validated_data):
        email = validated_data.get("email")
        country = validated_data.get("country")
        phone = validated_data.get("phone")
        auth_type = validated_data.get("auth_type")

        if auth_type == AuthTypeChoice.FACEBOOK:
            email_exists = User.objects.filter(email=email).exists()
            if email_exists:
                raise serializers.ValidationError(
                    {"email": ["Email already registered in another account!"]}
                )

        if auth_type == AuthTypeChoice.GOOGLE:
            email_exists = User.objects.filter(email=email).exists()
            if not email_exists:
                raise serializers.ValidationError({"email": ["Email not found!"]})

        country_obj = Country.objects.get(id=country)
        parse_number = phonenumbers.parse(phone, country_obj.alpha_2)
        number_is_valid = phonenumbers.is_valid_number(parse_number)

        if number_is_valid == False:
            raise serializers.ValidationError(
                {"phone": ["Phone number not valid for your country!"]}
            )

        return validated_data

    def save_data(self):
        email = self.validated_data.get("email")
        country = self.validated_data.get("country")
        phone = self.validated_data.get("phone")
        auth_type = self.validated_data.get("auth_type")
        social_id = self.validated_data.get("social_id", None)

        if auth_type == AuthTypeChoice.FACEBOOK:
            social_obj = SocialAuthData.objects.get(social_id=social_id)
            obj = {
                "email": email,
                "country": country,
                "phone": phone,
                "auth_type": auth_type,
                "social_id": social_id,
            }
            social_obj.signup_data = obj
            social_obj.save()
            return social_obj
        elif auth_type == AuthTypeChoice.GOOGLE:
            user = User.objects.get(email=email)
            country_obj = Country.objects.get(id=country)

            user.country = country_obj
            user.phone = phone
            user.save()
            return user
        return None


class SocialAuthVerifyConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    social_id = serializers.CharField(required=True)
    code = serializers.CharField(required=True)

    def validate(self, validated_data):
        email = validated_data.get("email")
        social_id = validated_data.get("social_id")
        code = validated_data.get("code")

        social_obj_exists = SocialAuthData.objects.filter(social_id=social_id).exists()

        if not social_obj_exists:
            raise serializers.ValidationError({"common": ["Invalid data!"]})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": ["Email exists!"]})

        try:
            verification_obj = Verification.objects.get(email=email)
        except:
            verification_obj = None

        if verification_obj is None:
            raise serializers.ValidationError({"email": ["Not found!"]})
        else:
            if verification_obj.code != int(code):
                raise serializers.ValidationError({"code": ["Invalid code!"]})
        return validated_data

    def create_user(self):
        email = self.validated_data.get("email")
        social_id = self.validated_data.get("social_id")

        social_obj = SocialAuthData.objects.get(social_id=social_id)
        signup_data = social_obj.signup_data

        country_obj = Country.objects.get(id=signup_data.get("country"))

        social_data = social_obj.data
        picture = social_data["picture"]["data"]["url"]

        user = User.objects.create(
            auth_type=AuthTypeChoice.FACEBOOK,
            full_name=social_data.get("name", None),
            email=email,
            phone=signup_data.get("phone", None),
            country=country_obj,
            social_image_url=picture,
            is_email_verified=True,
        )
        return user
