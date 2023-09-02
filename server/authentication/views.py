import datetime

from django.shortcuts import render
from django.core.files.images import get_image_dimensions
from django.conf import settings

from rest_framework import viewsets, mixins, generics
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters as rest_filter
from rest_framework.decorators import action

from wagtail.images.models import Image as wagtail_image


from django_filters import rest_framework as filters

from .serializers import *
from .models import *
from .permissions import *
from .social_auth import (
    google_authenticate,
    validate_social_signup,
    generate_token,
    facebook_authenticate,
)


class PublicUserApiViewset(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SocialAuthVerifyConfirmSerializer,
    )
    def social_auth_verify_confirm(self, request):
        """
        {
            "code": "",
            "email": "",
            "social_id": ""
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.create_user()
            token = generate_token(user)
            serializer_data = UserSerializer(user).data
            serializer_data["token"] = token
            return Response(serializer_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SocialAuthCompleteSerializer,
    )
    def complete_social_signup(self, request):
        """
        {
            "email": "", #if authtype == 2
            "country": "",
            "phone": "",
            "social_id": "", #if authtype == 2
            "auth_type": "1,2"
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            auth_type = int(request.data.get("auth_type", None))
            obj = serializer.save_data()
            if auth_type == AuthTypeChoice.GOOGLE:
                token = generate_token(obj)
                user_data = UserSerializer(obj).data
                user_data["token"] = token
                user_data["auth_type"] = AuthTypeChoice.GOOGLE
                return Response(user_data, status=status.HTTP_200_OK)
            elif auth_type == AuthTypeChoice.FACEBOOK:
                data = SocialAuthDataSerializer(obj).data
                data["auth_type"] = AuthTypeChoice.FACEBOOK
                User.send_verification_code(
                    User, email=request.data.get("email"), reason="verify"
                )
                return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=UserSerializer,
    )
    def facebook_signup(self, request):
        """
        {
            "code": "",
        }
        """
        auth_code = request.data.get("code", None)
        if not auth_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = facebook_authenticate(auth_code)
        auth_status, auth_type, user = validate_social_signup(
            user_data, auth_type=AuthTypeChoice.FACEBOOK
        )

        if auth_status == False:
            return Response(
                {"signin_status": False, "user_data": user_data},
                status=status.HTTP_200_OK,
            )
        elif auth_status == True:
            token = generate_token(user)
            serializer_data = UserSerializer(user).data
            serializer_data["token"] = token
            return Response(
                {"signin_status": True, "user": serializer_data},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"signin_status": False, "user": None, "user_data": user_data},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=UserSerializer,
    )
    def google_signup(self, request):
        """
        {
            "code": "",
        }
        """
        auth_code = request.data.get("code", None)
        if not auth_code:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        user_data = google_authenticate(auth_code)
        auth_status, auth_type, user = validate_social_signup(user_data)

        if auth_status == False:
            return Response(
                {"auth_type": auth_type}, status=status.HTTP_400_BAD_REQUEST
            )
        else:
            token = generate_token(user)
            serializer_data = UserSerializer(user).data
            serializer_data["token"] = token
            return Response(serializer_data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get"],
        permission_classes=(AllowAny,),
    )
    def social_auth_data(self, request):
        social_id = request.GET.get("social_id")
        if social_id:
            try:
                obj = SocialAuthData.objects.get(social_id=social_id)
            except:
                obj = None
            if obj:
                data = SocialAuthDataSerializer(obj).data
                return Response(data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SignUpSerializer,
    )
    def signup(self, request):
        """
        {
            "full_name": "",
            "email": "",
            "password": "",
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            User.send_verification_code(
                User, email=request.data.get("email"), reason="verify"
            )
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SendVerificationCodeSerializer,
    )
    def send_verification_code(self, request):
        """
        {
            "email": email,
            "user_checking": boolean(true/false),
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.send_code()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=VerifySerializer,
    )
    def verify_code(self, request):
        """
        {
            "email": email,
            "code": code,
            "user": {
                "full_name": "",
                "email": "",
                "password": ""
            }
        }
        """
        user_data = request.data.pop("user", None)
        if user_data:
            user_checking = False
            signup_user = user_data.get("email", None)
        else:
            user_checking = True
            signup_user = None

        serializer = self.serializer_class(
            data=request.data,
            context={"user_checking": user_checking, "signup_user": signup_user},
        )
        if serializer.is_valid():
            if user_data:
                verify_status = serializer.verify_code_signup()
                if verify_status:
                    signup_serializer = SignUpSerializer(data=user_data)
                    if signup_serializer.is_valid():
                        signup_serializer.save()
                        serializer.send_verify_confirm_email()
                        return Response(status=status.HTTP_200_OK)
                    return Response(
                        signup_serializer.errors, status=status.HTTP_400_BAD_REQUEST
                    )
            else:
                serializer.verify_code()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=SigninSerializer,
    )
    def signin(self, request):
        """
        {
            "username": username,
            "password": password,
            "user_type": 0,1
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, token = serializer.signin()
            data = UserSerializer(user).data
            data["token"] = token
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=AffiliateSigninSerializer,
    )
    def affiliate_signin(self, request):
        """
        {
            "username": username,
            "password": password,
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user, token = serializer.signin()
            data = UserSerializer(user).data
            data["token"] = token
            return Response(data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=(AllowAny,))
    def verify_code_for_forget_password(self, request):
        """
        {
            "email": email,
            "code": code,
        }
        """
        email = request.data.get("email", None)
        code = request.data.get("code", None)

        if email and code:
            verification_obj = Verification.objects.filter(
                email=email, code=code
            ).exists()
            if verification_obj:
                return Response(
                    {"verify_status": True, "verify_error_msg": None},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"verify_status": False, "verify_error_msg": "Invalid data!"},
                    status=status.HTTP_200_OK,
                )
        return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(AllowAny,),
        serializer_class=ForgetPasswordSerializer,
    )
    def forget_password(self, request):
        """
        {
            "email": email,
            "code": code,
            "password": new-password
        }
        """
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.forget_password()
            return Response(status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=(IsAuthenticated,),
        serializer_class=ChangePasswordSerializer,
    )
    def change_password(self, request):
        """
        {
            "old_password": old_password,
            "new_password": new_password,
            "new_password2": new_password2
        }
        """
        serializer = self.serializer_class(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            user = serializer.change_password()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"], permission_classes=(IsAuthenticated,))
    def upload_profile_image(self, request, pk=None):
        """
        {
            "image": image file
        }
        """
        user = request.user

        image = request.data.get("image")
        title = image.name
        width, height = get_image_dimensions(image)

        wagtail_img_obj = wagtail_image.objects.create(
            title=title, file=image, width=width, height=height
        )
        user.profile_image = wagtail_img_obj
        user.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=["get", "patch", "delete"],
        serializer_class=UserSerializer,
        permission_classes=(IsAuthenticated,),
    )
    def profile(self, request, pk=None):
        """
        {
            "full_name": "",
            "email": "",
        }
        """
        user = request.user

        if self.request.method == "GET":
            data = self.serializer_class(user).data
            return Response(data, status=status.HTTP_200_OK)
        elif self.request.method == "PATCH":
            serializer = self.serializer_class(
                instance=user, data=request.data, partial=True
            )
            if serializer.is_valid():
                user_obj = serializer.save()
                return Response(
                    UserSerializer(user_obj).data, status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif self.request.method == "DELETE":
            user.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
